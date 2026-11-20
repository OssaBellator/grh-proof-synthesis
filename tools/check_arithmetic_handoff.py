"""Check a curated arithmetic source graph and reproduce its offline receipt."""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, build_opener


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data" / "arithmetic-handoff.json"
REPO = "CocoSgt/riemann-hypothesis-lean"
REVISION = "0fb9869c6e6d7b54b67de803af0e0be29d37fc22"
RAW = f"https://raw.githubusercontent.com/{REPO}/{REVISION}/"
BLOB = f"https://github.com/{REPO}/blob/{REVISION}/"
MAX_FILE_BYTES = 128 * 1024
MAX_TOTAL_BYTES = 512 * 1024

# Source ID | bytes | SHA-256 | repository path.
SOURCE_SPEC = """
main | 433 | 017645ca448f2fd1f6fd5c4c2cb2c6e96e472725be13f6e180ca6e1574360939 | src/Main.lean
statements | 783 | 79ef7ca776e42abe1f46caee13ea09bd19f1e2d0b1620d8d5d200258f33b47bf | src/Statements.lean
wrappers | 740 | 1e734200b9b6a6d2a968743bd0c433d614bd6606cf538ac6d4f0ff70044dde53 | src/Supplements/Kernels/MainTheorems.lean
conclusion | 1213 | a5f71e107087e37b2c598709795b0f56c0a6741cf1e8ab99ee1f97e2fce0fe34 | src/Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean
every | 1215 | 31f6e49936226cfc3d71b15685347bd2874db0aef384e5cf4fea7d09ba68dc71 | src/Development/AutomorphicArithmetic/CharacterBoxes/EveryCharacter.lean
literature | 97393 | 246b74eeb03dae250c45b46c155b3590cb53c2bac86f5e35f4b74338db487068 | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean
handoff | 8752 | e761e876e3236895eec1b67b5a2118846ddfcc6883eed367ac6cc78523da15f2 | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/SiegelEisensteinSecondTermHypotheses.lean
theta-types | 28971 | 62209e957e734a32e4a85feb546cb2e8e7e087475d54fe5575b8fa7b4bd80197 | src/Development/AbelianVarietyTheory/BlockTheory/DivisorBase/WeilTensorModels.lean
theta-head | 2146 | 9db3d1af3aac449a4142cbd146a4bcb7b12fbb1fe3b1c73115a4fa274a87b6bf | src/Development/WeilBound/ThetaLifts/Reductions/FiniteClosure/TheoremKOfMod.lean
theta-assembly | 27212 | 388ed49b7854787ba11153c6fbdf7094da29e3f940fa9c61773342cb72707d1e | src/Development/WeilBound/ThetaLifts/SphericalLattices/SphericalClosure/CloseSph.lean
theta-leaves | 405 | d744817cdee7b91992ea1185f8147cb144fe8edff6275756e32901b22f2b47f0 | src/Development/WeilBound/ThetaLifts/AgreeOfLeaves.lean
eisenstein | 8967 | d73a7120fc8aa16f6a4f9f0d9f986455044454b274c9a391844811e145aea188 | src/Development/WeilBound/RepresentationTheoryGL/EisensteinSeries/SiegelEisensteinHalfPlane/SchwartzBruhatMajorants/SiegelMultOf.lean
siegel-weil | 452 | fcfc50f0151ae18442a877ab9193933f99b922a5d812aa7569ccc4665156f1dd | src/Development/WeilBound/CoreStatements/AutomorphicKernels/SiegelWeilFormula/SiegelWeilStandard/SiegelWeilStd.lean
hecke-one-type | 7458 | 3d2dbc2ba4ab93fd773d3aac39bdf805628276e7fad7d39c90d9c0b62d4d27af | src/Development/AbelianVarietyTheory/PublishedTheorems/TwistedTraceFormula/HeckeLEntireAndNonzeroAtOne.lean
hecke-one-proof | 8311 | 420dde5e03665d42fe60d154687af958ed02edbf7b3db5ab40389646585ce582 | src/Development/AbelianVarietyTheory/Proofs/TwistedOperators/HeckeLEntireAndNonzeroAtOneHolds.lean
hecke-one-wrapper | 1157 | 9e1fb005b142b4c7e2cb97fee064356baf36bf99591ecd1bf2eaab57683e3bae | src/Development/WeilBound/CoreStatements/StandardPublishedResults/StandardTheoremStatements/HeckeLEntireAndNonzeroAtOne.lean
covol-top | 2836 | 545f4dbcc8b67e0d001951fcad7abaa8250d335a64a6950adf5ce69fee5f30a0 | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/TopCovolSlim2Use.lean
covol-g | 6400 | f29362501bf62b9b6a7eb933aa0bdf9065414ecca014cf4a9da2970d791b4928 | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/TopCovolG.lean
covol-type | 6297 | a73cbdc50b441874d719358771398f999f21e720ef899a99b66c09b9bf72272b | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LiftLambdaBound.lean
covol-lambda | 3664 | a41e2f736d27da7fde44ef3bdb850a88217720acded5d5d910b7ac7a8a25039a | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/CoveringLambdaInvariantBound.lean
covol-steps-wrapper | 1318 | b44910310a652e4b6edc43be701af3e695b2f65f146b5096f05710bb82ea6d3a | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/CovolXOfStepsStatement.lean
covol-steps | 2912 | 91523ca83062a562c25a77e794e99d2028103fce290ca0749392aed99ea38c75 | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/CovolXOfSteps.lean
covol-estimate | 5827 | 840e9bdd6a0114433a9a8a7b42c52cc6f69cd5ab6604b3fa95750e3c580e90a7 | src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CovolumeFromGramAndBounds.lean
lambda-type | 15459 | f40c762ed8c2b18311d604540c15613e4a5969b1395dcab59b2854584fb6d3ae | src/Development/AbelianVarietyTheory/Definitions/Divisors/CovolXOfCovol.lean
parameters | 1674 | c1d3ba89b86a5e8e29274a27baaa7766ad50e103e462d72b835d3c6615d6259e | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/Prm1.lean
local-two-three | 2978 | dd8358fe7eae54e8029e7f0a990c3b8b3ad91c6fd31684581dbba64984770244 | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/At23OfAll.lean
local-two-three-type | 2482 | d7727aefd6cd01b68813e86b763e7393ae4712c97bb99df132264602e46f6fe5 | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/BoundAtTwoThreeFamilyFon.lean
grid | 5155 | 19afab8464c5823c489ac05c3b31350bb9fe8421e73f75e96968647f711f4794 | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/EvaluationGridOfJoin.lean
ll-forward | 1455 | 7e79c483b1f5c987425d180cc1502b177b5174b5dae4c4fb956ffc9e4131cec5 | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LlOf.lean
ll-type | 6283 | 4054d69535a55b8df339dee1ed766d38cb271ae87ce6033a8e0195ac577d9931 | src/Development/AutomorphicArithmetic/Foundations/LocalLanglands/IsRecTOfIsRec.lean
ll-exists | 3557 | 2411dd4cb455607d3f39761258ccde5c9e945443c421e69a626e4148a79824ab | src/Development/AutomorphicArithmetic/Foundations/LocalLanglands/LocalCentralUnits/RecTExists.lean
row | 433 | 0cfbca6cb7d1da543ee9d24c30faeeb3f68838f91c4f6c2c0e682e025c8b9a44 | src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/IntegralStructures/RowSrc.lean
row-type | 5507 | e3020031e884beef2eff18275019b7213a16f3c721242e9a79891b5396955719 | src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/TypeConditions/WeightsConjBis.lean
row-alias | 403 | 851c34b5611d4cf13499cafacfc3111ef71b1f642eb3feb00565ab40e0fd39d1 | src/Development/AutomorphicArithmetic/Foundations/UnitarySphericalFixing/SatakeParameters/RecT.lean
row-lift | 495 | 3f72f1644a6214bb5b90a5e9bac5e33b0474d52eb22f2f1841d443ed342531c2 | src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/IntegralStructures/GaloisRepresentationsOfThetaLift.lean
vwin-row | 515 | d2df45a5cf337190ae6f885e8e43056ae4e804ae8da250a2ab0abd64b1ca7080 | src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/VwinOfRow.lean
vwin-base-change | 487 | a8dbda049d3f53757e79628e6d3ec1b2ff3cc239057f596d2f87ca9f9f1c3905 | src/Development/AutomorphicArithmetic/Foundations/BaseChangeIdentities/DefiniteNHolds.lean
vwin-top | 6603 | f824d3f7873a493432bdfcbdc279fa82d70a6a9dbaac44c2a30316cada2eae3e | src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/TopMainZj.lean
vwin-window | 3721 | 576e18ba083451bcffe9e94075dc8d22ccfa6995fa8d30d68ea108b1cc910cf0 | src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/WindowBoundOfLiteratureLevel.lean
vwin-core | 2281 | 695927bf54a16053ae211e0d1f7ad26217806520d60f884459f9c0d7aac1460d | src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/HVCore.lean
vwin-counts | 2436 | 3c71cf0dabc617e3d1ab9fc04939c311e4242912407cdfbc71c8e0764563d558 | src/Development/AutomorphicArithmetic/AutomorphicVarieties/HeightAndVanishing/JointWinOfCounts.lean
vwin-joint | 7504 | ded642308ff9cd83eed14643f20899986c271c73f2ee900bccf6f7a32f3b350d | src/Development/AutomorphicArithmetic/AutomorphicVarieties/CMFieldExponentialBounds/AdmissibleOfPageN.lean
vwin-type | 3776 | 732c3347fb02e410cf9af8831afdbba1d230fc522c3dbbccdb4b708e5dde73db | src/Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean
top-plug | 1667 | 7d1d7972a4abe1284c5e4da9dd65a6eb605b06efb5e993b298fe5aaed88e9adf | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/TopPlug.lean
top-shape | 6555 | 9647d4cbe444f79de90c7a5371801e83c58a040499bf03fd61faf37be9e6eaa3 | src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/TopShape.lean
top-family | 2157 | 655762e90a0d7aae940774b631286a6cb942e59f68d7a3c350c05274487bf6ec | src/Development/AutomorphicArithmetic/CharacterBoxes/DesWin.lean
divisibility | 6424 | cefdce360890e26405199ef8db01d6b0c7e044c4ebebeb6bbcfd23de6148bde0 | src/Development/AutomorphicArithmetic/CharacterBoxes/DivinNOfHypV.lean
zero-free | 1791 | 349d9eafe63952c2fa4ccb2055bef7de0144d442c552196183fe48f01958f033 | src/Development/AutomorphicArithmetic/CharacterBoxes/ZeroFreeAllOfTopG.lean
zero-free-type | 7338 | d6b12bcbdc15c1b717c33a712474f9fca18c577a65c41fff2b2937534e5447ba | src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean
imprimitive | 1781 | 8de85415d0d139f23b2b50ba56c18ab3b3e29740f41e2d86eaf99b95765f512e | src/Development/AutomorphicArithmetic/CharacterBoxes/Imprimitive.lean
supply-chi | 697 | 70a11ba909e03b9153a6beacce24da22f3224b8192ec6980b7f27018961be81b | src/Development/AutomorphicArithmetic/CharacterBoxes/SupplyChi.lean
supply-field | 1830 | cd70757dd71088386ae322de0a4ce80adaeec30c2fcfe5f2ae03ae2b69e515b9 | src/Development/AutomorphicArithmetic/CharacterBoxes/HostOfField.lean
supply-proof | 8159 | b70c2177d57dfcd03f82784741813b7c6e6b525c69ffec5cae5527f03013a364 | src/Development/AutomorphicArithmetic/ShortNorms/supplyOfAdmOf.lean
win-pairs | 4570 | 41c1edf737bb6e1a4791d4440488a885889209db750698359ab4d1e237dc2f6e | src/Development/AutomorphicArithmetic/CharacterBoxes/WinPairs.lean
pair-types | 2421 | e5ddbc7f4573275caad502b8414dc3579ed904d1fa6c5f3848080bbd94fb3abb | src/Development/AutomorphicArithmetic/CharacterBoxes/PairGood.lean
pair-ex | 8552 | 8af18345e99c599e185472a0221b84acf33455b19ea1d77fe5bed311236f9890 | src/Development/AutomorphicArithmetic/MeanSquareBounds/pairEx.lean
pair-exists | 2782 | e4e59ce3542cdbde727aaef132c495d1aa20d99c42dee8cf058c3f5a407a8db7 | src/Development/AutomorphicArithmetic/MeanSquareBounds/PairExists.lean
pair-share | 3444 | dc43506b1872e1afb8892d25feb9062264c1dd929acc51838131e559a3e0de0b | src/Development/AutomorphicArithmetic/MeanSquareBounds/PairShare.lean
stage-one | 5255 | 5d3d6a56d035eb031bd207d4474a768b65dadf148579df0cb4815c51a1206819 | src/Development/AutomorphicArithmetic/MeanSquareBounds/Stage1Succ.lean
prime-bounds | 3089 | 5add5a8d499ab3c7d84e64e3ea1c529d09b7ecc472a7fa82e700881196861ec2 | src/Development/AutomorphicArithmetic/MeanSquareBounds/PrimeSetTwoBounds.lean
"""

# Node ID | role | declaration | source ID | lines | exact source anchor.
NODE_SPEC = """
main-grh | target | LFunction_eq_zero_re | main | 10 | DirichletLZerosOnLine := claimAll.2.1
main-half | target | LFunction_ne_zero_of_half_lt_re | main | 8 | DirichletLNonvanishingRightOfHalf := allChi
main-rh | target | riemannHypothesis | main | 4 | RiemannHypothesis := rhOfAll
half-type | proposition | DirichletLNonvanishingRightOfHalf | statements | 6-7 | def DirichletLNonvanishingRightOfHalf
rh-wrapper | forwarder | rhOfAll | wrappers | 9 | Formalism.VW.rh_of_every allChi
claim-all | record-constructor | claimAll | wrappers | 15-16 | ⟨allChi, Claim.strip allChi, Claim.zeta allChi⟩
all-chi | forwarder | allChi | wrappers | 7 | := UpperTheory.FinalTheorems.everyCharacter
every-char | forwarder | UpperTheory.FinalTheorems.everyCharacter | conclusion | 10-11 | everyCharacter_of_row UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter
every-type | proposition | UpperTheory.EveryCharacter | every | 13-14 | DirichletCharacter.LFunction χ s ≠ 0
row-wrapper | forwarder | UpperTheory.FinalTheorems.everyCharacter_of_row | conclusion | 7-8 | ⟨h, UpperTheory.Zero.LLC.recTExists, h⟩
row-proof | forwarder | UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter | row | 4-6 | galoisRepresentations_of_thetaLift UpperTheory.TP.K.tLiftK
row-lift | forwarder | UpperTheory.Gal.Int.galoisRepresentations_of_thetaLift | row-lift | 4-6 | galoisLocalGlobalStrong_of_geometry_lift UpperTheory.Gal.Int.Geo.geoOne_holds up
row-alias | proposition | UpperTheory.One.M.Row | row-alias | 6 | def UpperTheory.One.M.Row
row-type | proposition | UpperTheory.GalStar.Row0b | row-type | 54-73 | def Row0b : Prop
literature-input | record | UpperTheory.LiteratureTheorems.OpenLiteratureStatements | literature | 215-218 | structure UpperTheory.LiteratureTheorems.OpenLiteratureStatements : Prop
literature-call | forwarder | UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin | literature | 810-813 | theorem UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin
handoff | forwarder | UpperTheory.Lit.every_character_of_theta_integrals_local_matching | handoff | 39-73 | theorem every_character_of_theta_integrals_local_matching
eigen-bundle | record-constructor | UpperTheory.LiteratureTheorems.published_results_eigen | literature | 666-726 | UnitaryGroupThirdPlaceHypotheses where
local-bundle | record-constructor | UpperTheory.LiteratureTheorems.published_results_first | literature | 727-780 | GlobalTheory.FunPr.ThetaLocalInputs where
theta-first | projection | (theta_integrals_agree_and_local_matching_of_literature O).1 | literature | 811 | theta_integrals_agree_and_local_matching_of_literature O).1
theta-second | projection | (theta_integrals_agree_and_local_matching_of_literature O).2 | literature | 811 | theta_integrals_agree_and_local_matching_of_literature O).2
theta-pair | forwarder | UpperTheory.LiteratureTheorems.theta_integrals_agree_and_local_matching_of_literature | literature | 565-566 | PositivityTheory.ThKR.theoremK_head2
theta-agree | proposition | GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.ThetaIntegralsAgree | theta-types | 585-592 | def ThetaIntegralsAgree : Prop
local-match | proposition | GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.LocalMatching | theta-types | 581-583 | def LocalMatching : Prop
theta-decay | estimate | GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.Decay | theta-types | 498-501 | def Decay : Prop
theta-scalar | proposition | GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.OneConst | theta-types | 491-505 | def OneConst : Prop
theta-steps | proposition | GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.StepBeta / StepAlpha | theta-types | 552-579 | def StepAlpha
theta-head | forwarder | PositivityTheory.ThKR.theoremK_head2 | theta-head | 26-27 | theoremK_head2_of_mod PositivityTheory.Sph.modSt2 h11 h12
theta-mod | conditional-proof | PositivityTheory.ThKR.theoremK_head2_of_mod | theta-head | 14-20 | Tr.closeSph
theta-assembly | mathematical-proof | PositivityTheory.Sph.Tr.closeSph | theta-assembly | 28-193 | theorem PositivityTheory.Sph.Tr.closeSph
theta-leaves | record-constructor | PositivityTheory.ThKG.agree_of_leaves | theta-leaves | 7-8 | ⟨agree_of_parts hd L.kConst hc L.kBeta L.kAlpha, matching_of_parts L.kReal L.kFin⟩
eis | forwarder | UpperTheory.LiteratureTheorems.eis_bl_of_literature | literature | 561-562 | PositivityTheory.RgEis.Hd.eisBL
sw | forwarder | UpperTheory.LiteratureTheorems.siegel_weil_std_of_literature | literature | 563-564 | PositivityTheory.SiegelWeilFormula.Fin.siegelWeilStd
eis-proof | mathematical-proof | PositivityTheory.RgEis.Hd.eisBL | eisenstein | 101-113 | theorem eisBL : GlobalTheory.ThK.Dbl.EisBL
sw-proof | mathematical-proof | PositivityTheory.SiegelWeilFormula.Fin.siegelWeilStd | siegel-weil | 6-8 | siegelWeilStd_of_ct (Act.ctSplit_of kfour.auxEx kfour.coefEx)
hecke-one-wrapper | forwarder | PositivityTheory.Stage1.PM.heckeLEntireAndNonzeroAtOne | hecke-one-wrapper | 18-19 | GlobalTheory.Published.HeckeLEntireAndNonzeroAtOne_holds
hecke-one-type | proposition | GlobalTheory.Published.HeckeLEntireAndNonzeroAtOne | hecke-one-type | 19-31 | def HeckeLEntireAndNonzeroAtOne : Prop
hecke-one-proof | mathematical-proof | GlobalTheory.Published.HeckeLEntireAndNonzeroAtOne_holds | hecke-one-proof | 112-134 | theorem _root_.GlobalTheory.Published.HeckeLEntireAndNonzeroAtOne_holds
hecke-one-literature | forwarder | UpperTheory.LiteratureTheorems.hecke_l_entire_and_nonzero_at_one_of_literature | literature | 427-428 | PositivityTheory.Stage1.PM.heckeLEntireAndNonzeroAtOne
nonempty | conditional-proof | UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound | handoff | 44-68 | theorem nonempty_hyps_definite_side_of_closed_bound
linked-bound | conditional-proof | UpperTheory.N.boundAtTwoThree_linked_of_recT | local-two-three | 19-26 | theorem boundAtTwoThree_linked_of_recT
linked-bound-type | proposition | GlobalTheory.NLink.BoundAtTwoThreeFamilyFonAlt | local-two-three-type | 25-28 | def BoundAtTwoThreeFamilyFonAlt
link-parameters | forwarder | GlobalTheory.Mem.Top.Bl.parametersOfDependence | parameters | 20-21 | def parametersOfDependence
eval-grid | conditional-proof | GlobalTheory.Mem.LiteralAutomorphy.evaluation_grid_of_join | grid | 23-44 | theorem evaluation_grid_of_join
covol | conditional-proof | SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt | covol-top | 16-22 | theorem topCovolSlim2_use_alt_alt
covol-type | proposition | GlobalTheory.CovTop.CovolumeBoundOfX | covol-type | 17-61 | def CovolumeBoundOfX : Prop
covol-g | conditional-proof | SelfIntersectionVolumeEstimates.topCovolG_alt_alt | covol-g | 39-58 | theorem topCovolG_alt_alt
covol-pubs | record-constructor | UpperTheory.LiteratureTheorems.published_results_arithmetic | literature | 781-809 | GlobalTheory.CovTop.PublishedHodgeBundleTheorems where
covol-assembly-wrapper | forwarder | GlobalTheory.T.covolX_of_truncation_badSet_lambda_lowBound | covol-steps-wrapper | 11-12 | Assembly.covolX_of_lift_bounds_and_coreLe
covol-assembly | conditional-proof | GlobalTheory.CovTop.Assembly.covolX_of_lift_bounds_and_coreLe | covol-steps | 16-40 | have main := lcv_le
covol-inequality | estimate | GlobalTheory.CovTop.Assembly.lcv_le | covol-estimate | 39-84 | theorem lcv_le
covol-loss | estimate | GlobalTheory.CovTop.Assembly.exists_loss_le | covol-estimate | 25-34 | theorem exists_loss_le
lift-lambda | estimate | GlobalTheory.T.liftLambdaBound_of_gram_meas | covol-lambda | 21-45 | integral_cusp_slope_power_bound_alt_alt
lambda-type | estimate | GlobalTheory.CovTop.LamAt | lambda-type | 73 | def LamAt (A : ℝ) : Prop
ll-literature | forwarder | UpperTheory.LiteratureTheorems.local_langlands_gl_recT_exists_of_literature | literature | 313-314 | UpperTheory.One.M.New.llOf_alt
ll-adapter | forwarder | UpperTheory.One.M.New.llOf_alt | ll-forward | 18-21 | fun h _ _ _ _ _ _ _ _ _ _ _ => h
ll-projection | projection | UpperTheory.LiteratureTheorems.local_langlands_recT_exists_of_literature | literature | 283-284 | O.localLanglandsExists
ll-witness | mathematical-proof | UpperTheory.Zero.LLC.recTExists | ll-exists | 20-66 | theorem UpperTheory.Zero.LLC.recTExists
ll-type | proposition | UpperTheory.Zero.LLC.RecTExists | ll-type | 55-80 | def RecTExists : Prop
vwin | proposition | UpperTheory.Top.VWin | vwin-type | 39-49 | ∀ ψ : PChar, VWinAt ψ 401
vwin-bound | estimate | UpperTheory.Top.VVle | vwin-type | 12-17 | def VVle
vwin-row | forwarder | UpperTheory.One.vwin_of_row | vwin-row | 4-5 | UpperTheory.One.Join.automorphic_window_of_inputs
vwin-base-change | forwarder | UpperTheory.BaseChangeIdentities.baseChangeN | vwin-base-change | 5-6 | baseChangeN_of UpperTheory.HeckeLevelFrameExistence.candFin
vwin-top | forwarder | UpperTheory.One.Join.automorphic_window_of_inputs | vwin-top | 71-74 | theorem UpperTheory.One.Join.automorphic_window_of_inputs
vwin-from-inputs | record-constructor | UpperTheory.One.Join.v_window_of_depth_zero_residual_bc_cm | vwin-top | 55-58 | v_window_of_literal_automorphy_n ⟨
vwin-window | forwarder | UpperTheory.V.v_window_of_literal_automorphy_n | vwin-window | 33-34 | theorem UpperTheory.V.v_window_of_literal_automorphy_n
vwin-patching | conditional-proof | UpperTheory.V.HV.DescentVanishingReductions.v_window_of_automorphy_csd_ss_mono_odd | vwin-window | 30-31 | published_hypotheses_from_patching_alt hN
vwin-descent | conditional-proof | UpperTheory.V.HV.DescentVanishingReductions.vwin_of_hypotheses_H_E_alt | vwin-window | 25-29 | UpperTheory.V.HV.Core.of_four_alt
vwin-core | conditional-proof | UpperTheory.V.HV.Core.of_four_alt | vwin-core | 18-22 | exact vwin_of_counts
vwin-counts | conditional-proof | UpperTheory.V.HV.vwin_of_counts | vwin-counts | 25-33 | vwin_of_joint (jointWin_of_counts
vwin-joint | conditional-proof | UpperTheory.V.vwin_of_joint | vwin-joint | 41-133 | theorem vwin_of_joint (hJ : JointWin 401) (hc : ThmBc 401)
top-plug | forwarder | UpperTheory.Top.every_character_of_green_v_win | top-plug | 16-18 | UpperTheory.Top.imprimitive
primitive-bridge | conditional-proof | UpperTheory.Top.zero_free_all_of_green_v_win | top-plug | 12-15 | UpperTheory.Top.zeroFreeAll_of_topG
imprimitive | conditional-proof | UpperTheory.Top.imprimitive | imprimitive | 5-35 | theorem UpperTheory.Top.imprimitive
zero-free | conditional-proof | UpperTheory.Top.zeroFreeAll_of_topG | zero-free | 26-34 | zeroFreeOn_of_tiedWin_cyc
zero-free-type | proposition | Formalism.HC.ZeroFreeAll | zero-free-type | 11-18 | def ZeroFreeAll : Prop
shape | conditional-proof | UpperTheory.Top.shape_closed_link_n_of_green | top-shape | 33-55 | theorem UpperTheory.Top.shape_closed_link_n_of_green
family | conditional-proof | UpperTheory.Top.topDesWin | top-family | 11-31 | theorem topDesWin
divisibility | conditional-proof | UpperTheory.Top.divinN_of_hypV | divisibility | 117-130 | exact h6 x g6
log-square | estimate | UpperTheory.Top.log_sq_le_rpow | divisibility | 59-74 | Real.log x ^ 2 ≤ x ^ eps
supply-chi | conditional-proof | UpperTheory.Top.supplyChi | supply-chi | 8-16 | theorem UpperTheory.Top.supplyChi
supply | forwarder | UpperTheory.Top.supplyOfAdm | supply-field | 17-23 | UpperTheory.T3.supplyOfAdmOf UpperTheory.Top.hostOfField
supply-proof | conditional-proof | UpperTheory.T3.supplyOfAdmOf | supply-proof | 24-29 | hV QH.pairEx
win-pairs | conditional-proof | UpperTheory.Top.winPairs | win-pairs | 5-13 | VWinAt ψ 401 → PairEx
pair-types | estimate | UpperTheory.Top.PairGood / PairEx | pair-types | 12-30 | structure PairGood
pair-ex | mathematical-proof | QH.pairEx | pair-ex | 112-169 | theorem pairEx :
pair-exists | mathematical-proof | QH.pair_exists | pair-exists | 9-49 | theorem pair_exists :
pair-share | mathematical-proof | QH.pair_share | pair-share | 26-52 | theorem pair_share :
stage-one | estimate | QH.stage1 | stage-one | 36-39 | ¬ GoodQ N₀ C τ Y (Y ^ K) (Y ^ (ε / 5)) q
good-q | proposition | QH.GoodQ | prime-bounds | 48-49 | def GoodQ
box-all | proposition | QH.BoxAll | prime-bounds | 32-39 | def BoxAll
"""

# Consumer | relation | dependency | argument/field | source ID | lines | exact anchor.
EDGE_SPEC = """
main-grh | projects | claim-all | second conjunct via .2.1 | main | 10 | claimAll.2.1
main-half | calls | all-chi | shared half-plane proof | main | 8 | := allChi
main-half | type | half-type | public proposition | main | 8 | DirichletLNonvanishingRightOfHalf
main-rh | calls | rh-wrapper | zeta specialization | main | 4 | := rhOfAll
rh-wrapper | supplies | all-chi | argument of rh_of_every | wrappers | 9 | rh_of_every allChi
claim-all | supplies | all-chi | argument of Claim.strip for the middle conjunct | wrappers | 16 | Claim.strip allChi
all-chi | calls | every-char | shared arithmetic proof | wrappers | 7 | := UpperTheory.FinalTheorems.everyCharacter
every-char | type | every-type | output proposition | conclusion | 10 | : UpperTheory.EveryCharacter
every-char | calls | row-wrapper | apply conditional theorem | conclusion | 11 | everyCharacter_of_row UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter
every-char | supplies | row-proof | actual row input | conclusion | 11 | UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter
row-proof | calls | row-lift | parameterized by the named theta-lift input | row | 6 | galoisRepresentations_of_thetaLift UpperTheory.TP.K.tLiftK
row-proof | type | row-type | specialized to recT | row | 6 | UpperTheory.GalStar.Row0b recT
row-alias | type | row-type | specialize to IsRecT | row-alias | 6 | UpperTheory.GalStar.Row0b fun h rc => UpperTheory.Zero.LLC.IsRecT h rc
row-wrapper | calls | literature-call | invoke literature handoff | conclusion | 8 | UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin
row-wrapper | assembles | literature-input | constructor arguments are row, recTExists, row | conclusion | 8 | ⟨h, UpperTheory.Zero.LLC.recTExists, h⟩
row-wrapper | supplies | ll-witness | middle constructor field | conclusion | 8 | ⟨h, UpperTheory.Zero.LLC.recTExists, h⟩
row-wrapper | supplies | vwin-row | VWin from the same row | conclusion | 8 | (UpperTheory.One.vwin_of_row h)
literature-input | type | row-alias | two fields of type Row | literature | 215-218 | _root_.UpperTheory.One.M.Row
literature-call | calls | handoff | seven-argument application | literature | 810-813 | _root_.UpperTheory.Lit.every_character_of_theta_integrals_local_matching
literature-call | supplies | eigen-bundle | P | literature | 811 | (_root_.UpperTheory.LiteratureTheorems.published_results_eigen O)
literature-call | supplies | local-bundle | F | literature | 811 | (_root_.UpperTheory.LiteratureTheorems.published_results_first O)
literature-call | supplies | theta-first | hA | literature | 811 | (_root_.UpperTheory.LiteratureTheorems.theta_integrals_agree_and_local_matching_of_literature O).1
literature-call | supplies | theta-second | hM | literature | 811 | (_root_.UpperTheory.LiteratureTheorems.theta_integrals_agree_and_local_matching_of_literature O).2
literature-call | supplies | covol | hX | literature | 812 | _root_.SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt
literature-call | supplies | ll-literature | hL | literature | 813 | (_root_.UpperTheory.LiteratureTheorems.local_langlands_gl_recT_exists_of_literature O) hV
literature-call | forwarded | vwin | hV unchanged | literature | 810-813 | (_root_.UpperTheory.LiteratureTheorems.local_langlands_gl_recT_exists_of_literature O) hV
handoff | type | theta-agree | hA | handoff | 69 | WeilTensorModels.ThetaIntegralsAgree
handoff | type | local-match | hM | handoff | 70 | WeilTensorModels.LocalMatching
handoff | type | covol-type | hX | handoff | 70 | GlobalTheory.CovTop.CovolumeBoundOfX
handoff | type | ll-type | hL | handoff | 70 | UpperTheory.Zero.LLC.RecTExists
handoff | type | vwin | hV | handoff | 70 | (hV : VWin)
handoff | type | every-type | result | handoff | 71 | UpperTheory.EveryCharacter :=
handoff | calls | top-plug | Green input, hV, and assembled data | handoff | 72 | every_character_of_green_v_win (GlobalTheory.GreenBridge.green_of_regular P.greenRegularCharacters) hV
handoff | forwarded | vwin | hV passed unchanged to top plug | handoff | 72 | P.greenRegularCharacters) hV
handoff | calls | nonempty | P F hA hM hX hL and linked bound | handoff | 73 | nonempty_hyps_definite_side_of_closed_bound P F hA hM hX hL
handoff | supplies | linked-bound | uses P.nLink for each cDep | handoff | 73 | boundAtTwoThree_linked_of_recT P.nLink
handoff | calls | link-parameters | parameters indexed by hL and cDep | handoff | 73 | parametersOfDependence hL cDep
nonempty | calls | eval-grid | consumes hA and hM with other premises | handoff | 52-54 | evaluation_grid_of_join F.howeDualityReal hM F C.join C.fe hA
linked-bound | type | linked-bound-type | family bound under LinkedAt and SlotNormCondition | local-two-three | 24-26 | GlobalTheory.NLink.BoundAtTwoThreeFamilyFonAlt Fm
theta-first | projects | theta-pair | And.left | literature | 811 | theta_integrals_agree_and_local_matching_of_literature O).1
theta-second | projects | theta-pair | And.right | literature | 811 | theta_integrals_agree_and_local_matching_of_literature O).2
theta-first | type | theta-agree | left conjunct, hA | literature | 565 | WeilTensorModels.ThetaIntegralsAgree ∧
theta-second | type | local-match | right conjunct, hM | literature | 565 | ∧ GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.LocalMatching
theta-agree | requires | theta-decay | for every IsTriple | theta-types | 585-588 | → Decay B G om om' ∧
theta-agree | requires | theta-scalar | for every matching pair of maps | theta-types | 587-588 | → OneConst B G X om om' R Rf ∧ Coinv
theta-agree | requires | theta-steps | two separately quantified sign triples | theta-types | 589-592 | StepAlpha σ e₁ e₂ s
theta-pair | calls | theta-head | bundle wrapper | literature | 565-566 | PositivityTheory.ThKR.theoremK_head2
theta-pair | supplies | eis | EisBL argument | literature | 566 | eis_bl_of_literature O
theta-pair | supplies | sw | SiegelWeilStd argument | literature | 566 | siegel_weil_std_of_literature O
eis | calls | eis-proof | O unused by this wrapper | literature | 561-562 | PositivityTheory.RgEis.Hd.eisBL
sw | calls | sw-proof | O unused by this wrapper | literature | 563-564 | PositivityTheory.SiegelWeilFormula.Fin.siegelWeilStd
theta-head | calls | theta-mod | supplies modSt2 and forwards EisBL and SiegelWeilStd | theta-head | 26-27 | theoremK_head2_of_mod PositivityTheory.Sph.modSt2 h11 h12
theta-mod | calls | theta-assembly | supplies local and global input terms | theta-head | 14-20 | Tr.closeSph
theta-assembly | calls | theta-leaves | decay, coinvariants and constructed leaves | theta-assembly | 192-193 | agree_of_leaves h_Weil6_ThKG_Leaves h_GlobalTheory_ThK_KDecay h_GlobalTheory_ThK_KCoinv
theta-leaves | assembles | theta-agree | agree_of_parts | theta-leaves | 7-8 | agree_of_parts hd L.kConst hc L.kBeta L.kAlpha
theta-leaves | assembles | local-match | matching_of_parts | theta-leaves | 7-8 | matching_of_parts L.kReal L.kFin
local-bundle | assembles | hecke-one-literature | heckeLEntireAndNonzeroAtOne field | literature | 756 | heckeLEntireAndNonzeroAtOne := (_root_.UpperTheory.LiteratureTheorems.hecke_l_entire_and_nonzero_at_one_of_literature O)
hecke-one-literature | calls | hecke-one-wrapper | O unused by this wrapper | literature | 427-428 | PositivityTheory.Stage1.PM.heckeLEntireAndNonzeroAtOne
hecke-one-wrapper | calls | hecke-one-proof | delegates to holds theorem | hecke-one-wrapper | 18-19 | GlobalTheory.Published.HeckeLEntireAndNonzeroAtOne_holds
hecke-one-proof | type | hecke-one-type | nonvanishing at 1 for nontrivial unitary Hecke characters | hecke-one-proof | 112 | : GlobalTheory.Published.HeckeLEntireAndNonzeroAtOne
theta-assembly | supplies | hecke-one-proof | input of polynomial vanishing theorem | theta-assembly | 150 | GlobalTheory.Published.HeckeLEntireAndNonzeroAtOne_holds
covol | type | covol-type | conclusion | covol-top | 16 | GlobalTheory.CovTop.CovolumeBoundOfX
literature-call | supplies | covol-pubs | record supplied to the covolume producer | literature | 812 | published_results_arithmetic O
covol | calls | covol-g | assemble the geometric and height inputs | covol-top | 18-22 | SelfIntersectionVolumeEstimates.topCovolG_alt_alt
covol-g | calls | covol-assembly-wrapper | assemble the lift bounds | covol-g | 58 | covolX_of_truncation_badSet_lambda_lowBound
covol-g | supplies | lift-lambda | actual lambda-bound producer | covol-g | 58 | liftLambdaBound_of_gram_meas hP gram meas
covol-assembly-wrapper | calls | covol-assembly | same conditional type | covol-steps-wrapper | 12 | Assembly.covolX_of_lift_bounds_and_coreLe
covol-assembly | calls | covol-inequality | apply at each admissible point and lift index | covol-steps | 27-33 | have main := lcv_le p i
covol-assembly | supplies | covol-loss | use fixed exponents before x and lift index | covol-steps | 25-27 | exists_loss_le (show 0 < Fm.ez / 7 by positivity) A B (C1 + C2 + 1)
covol-inequality | requires | lambda-type | lambda bound at the chosen lift index | covol-estimate | 39-43 | (hL : LamAt p i A)
ll-literature | calls | ll-adapter | eleven ancillary arguments appear at the call | literature | 313-314 | _root_.UpperTheory.One.M.New.llOf_alt
ll-literature | supplies | ll-projection | first argument, returned unchanged | literature | 314 | (_root_.UpperTheory.LiteratureTheorems.local_langlands_recT_exists_of_literature O)
ll-adapter | forwarded | ll-type | returns its first RecTExists proof | ll-forward | 18-21 | fun h _ _ _ _ _ _ _ _ _ _ _ => h
ll-projection | projects | literature-input | O.localLanglandsExists | literature | 283-284 | O.localLanglandsExists
ll-witness | type | ll-type | explicit proof supplied by row wrapper | ll-exists | 20-22 | UpperTheory.Zero.LLC.RecTExists := by
vwin-row | calls | vwin-top | OpenImageCondition.mk h, baseChangeN, h | vwin-row | 4-5 | automorphic_window_of_inputs (UpperTheory.LiteratureTheorems.OpenImageCondition.mk h) UpperTheory.BaseChangeIdentities.baseChangeN h
vwin-row | supplies | vwin-base-change | middle argument | vwin-row | 5 | UpperTheory.BaseChangeIdentities.baseChangeN h
vwin-row | type | vwin | conclusion | vwin-row | 4 | : UpperTheory.Top.VWin
vwin-top | calls | vwin-from-inputs | supplies CM bundle with the other arguments | vwin-top | 71-74 | v_window_of_depth_zero_residual_bc_cm O bc gal
vwin-from-inputs | calls | vwin-window | supplies assembled local, automorphic, cohomological and CM record | vwin-top | 55-58 | UpperTheory.V.v_window_of_literal_automorphy_n
vwin-window | calls | vwin-patching | forwards the literature record | vwin-window | 33-34 | v_window_of_automorphy_csd_ss_mono_odd hN
vwin-patching | calls | vwin-descent | supplies the result of patching | vwin-window | 30-31 | vwin_of_hypotheses_H_E_alt
vwin-descent | calls | vwin-core | Lemma K and counts I, II, III, V | vwin-window | 25-29 | UpperTheory.V.HV.Core.of_four_alt
vwin-core | calls | vwin-counts | ThmBab specialized to 401 | vwin-core | 18-22 | exact vwin_of_counts
vwin-counts | calls | vwin-joint | JointWin 401 and ThmBc 401 | vwin-counts | 30-33 | vwin_of_joint (jointWin_of_counts
vwin-joint | type | vwin | iterates over ψ via vwinAt_of_joint | vwin-joint | 131-133 | exact vwinAt_of_joint (by norm_num) hJ hc ψ
vwin | requires | vwin-bound | VAt at each x in the selected window | vwin-type | 41-49 | VVle E ⌊x ^ Ct⌋₊
top-plug | calls | primitive-bridge | primitive nonvanishing before level change | top-plug | 16-18 | zero_free_all_of_green_v_win hG hV h
top-plug | calls | imprimitive | conductor and extra Euler factors | top-plug | 18 | UpperTheory.Top.imprimitive
primitive-bridge | calls | shape | build the TopG input using Green | top-plug | 14-15 | UpperTheory.Top.shape_closed_link_n_of_green hG
primitive-bridge | calls | zero-free | uses la = 3/2 | top-plug | 14-15 | zeroFreeAll_of_topG (la := 3 / 2)
primitive-bridge | supplies | supply-chi | supplies each host from hV ψ | top-plug | 15 | UpperTheory.Top.supplyChi ψ (hV ψ)
zero-free | type | zero-free-type | source primitive conclusion | zero-free | 26 | : ZeroFreeAll := by
imprimitive | type | zero-free-type | consumes primitive half-plane nonvanishing | imprimitive | 5-10 | ZeroFreeAll →
shape | calls | family | combine link hypotheses | top-shape | 52-55 | exact UpperTheory.Top.topDesWin
family | calls | divisibility | uses hV for family input HypV | top-family | 29 | divinN_of_hypV Fm h0
divisibility | supplies | log-square | eventual bound used in divinN_at at scale x | divisibility | 122-130 | obtain ⟨x6, h6⟩ := log_sq_le_rpow heps
supply-chi | calls | supply | combine window and admissible ranks | supply-chi | 10-16 | refine supplyOfAdm ψ hψ
supply | calls | supply-proof | instantiates host producer | supply-field | 23 | UpperTheory.T3.supplyOfAdmOf UpperTheory.Top.hostOfField
supply-proof | calls | win-pairs | combines distinct VWinAt and PairEx inputs | supply-proof | 29 | hV QH.pairEx
supply-proof | supplies | pair-ex | actual prime-pair producer | supply-proof | 29 | QH.pairEx
win-pairs | requires | pair-types | quantified existence of good prime pairs | win-pairs | 5-13 | VWinAt ψ 401 → PairEx
win-pairs | requires | vwin | individual character specialization | win-pairs | 5-13 | VWinAt ψ 401 → PairEx
pair-ex | type | pair-types | PairEx | pair-ex | 112-114 | UpperTheory.Top.PairEx := by
pair-ex | calls | pair-exists | selected q and d via GoodQ and GoodD | pair-ex | 115-130 | obtain ⟨C, hC, hpair⟩ := pair_exists
pair-exists | calls | pair-share | applies pair_share at eta = 1/2 | pair-exists | 13-15 | obtain ⟨C, hC, H⟩ := pair_share
pair-share | calls | stage-one | first prime selection | pair-share | 32-36 | obtain ⟨C1, hC1, h1⟩ := stage1
stage-one | type | good-q | bound the bad subset | stage-one | 38-39 | ¬ GoodQ N₀ C τ Y (Y ^ K) (Y ^ (ε / 5)) q
good-q | requires | box-all | for each base character at level N₀ | prime-bounds | 48-49 | BoxAll (N₀ * Real.exp z)
"""

HANDOFF_SIGNATURE = """theorem every_character_of_theta_integrals_local_matching (P : _root_.GlobalTheory.Fc.S0.UnitaryGroupThirdPlaceHypotheses) (F : _root_.GlobalTheory.FunPr.ThetaLocalInputs) (hA : GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.ThetaIntegralsAgree)
    (hM : GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.LocalMatching) (hX : _root_.GlobalTheory.CovTop.CovolumeBoundOfX) (hL : _root_.UpperTheory.Zero.LLC.RecTExists) (hV : VWin) :
    UpperTheory.EveryCharacter"""

NODE_ROLES = {
    "target", "forwarder", "record", "record-constructor", "projection",
    "mathematical-proof", "proposition", "estimate", "conditional-proof",
}
RELATIONS = {
    "calls", "supplies", "projects", "forwarded", "type", "assembles",
    "requires", "instantiates",
}


def rows(spec):
    for line in spec.strip().splitlines():
        yield line.split(" | ")


def location(source_id, span, anchor):
    limits = [int(part) for part in span.split("-")]
    return {"source_id": source_id, "lines": [limits[0], limits[-1]], "anchor": anchor}


def pinned_sources():
    return [
        {
            "id": source_id, "path": path, "bytes": int(size), "sha256": digest,
            "raw_url": RAW + quote(path), "repo_url": BLOB + quote(path),
        }
        for source_id, size, digest, path in rows(SOURCE_SPEC)
    ]


def build_registry():
    nodes = [
        {
            "id": node_id, "role": role, "name": name, "status": "source-inspected",
            "evidence": location(source_id, span, anchor),
        }
        for node_id, role, name, source_id, span, anchor in rows(NODE_SPEC)
    ]
    nodes.append({
        "id": "author-iteration", "role": "research-question", "status": "hypothetical",
        "name": "Identify a source bound uniform over the author's proposed repeated theta lifts",
    })
    edges = [
        {
            "from": consumer, "to": dependency, "relation": relation, "detail": detail,
            "status": "source-backed", "evidence": location(source_id, span, anchor),
        }
        for consumer, relation, dependency, detail, source_id, span, anchor in rows(EDGE_SPEC)
    ]
    edges.append({
        "from": "lift-lambda", "to": "author-iteration", "relation": "possible-connection",
        "status": "inferred", "detail": "Quantifier and normalization comparison remains open",
    })
    return {
        "schema_version": 1, "revision": REVISION, "scope": "curated source text; no elaboration",
        "sources": pinned_sources(), "nodes": nodes, "edges": edges,
    }


def unique_ids(items):
    ids = {item["id"] for item in items}
    if len(ids) != len(items):
        raise ValueError("Duplicate ID")
    return ids


def validate_location(evidence, source_ids):
    if evidence["source_id"] not in source_ids:
        raise ValueError(f"Unknown source {evidence['source_id']}")
    first, last = evidence["lines"]
    if type(first) is not int or type(last) is not int or not 1 <= first <= last:
        raise ValueError("Invalid source line range")
    if not isinstance(evidence["anchor"], str) or not evidence["anchor"].strip():
        raise ValueError("Empty source anchor")


def validate_registry(data):
    if data["schema_version"] != 1 or data["revision"] != REVISION:
        raise ValueError("Unknown receipt schema or revision")
    sources = data["sources"]
    if sources != pinned_sources():
        raise ValueError("Source pins differ from the fixed allowlist")
    source_ids = unique_ids(sources)
    node_ids = unique_ids(data["nodes"])
    hypotheses = set()
    for node in data["nodes"]:
        if not node["name"].strip():
            raise ValueError("Empty node name")
        if node["status"] == "source-inspected" and node["role"] in NODE_ROLES:
            validate_location(node["evidence"], source_ids)
        elif (node["status"], node["role"]) == ("hypothetical", "research-question"):
            if "evidence" in node:
                raise ValueError("Hypothetical node has source evidence")
            hypotheses.add(node["id"])
        else:
            raise ValueError("Invalid node status or role")

    seen = set()
    for edge in data["edges"]:
        endpoints = {edge["from"], edge["to"]}
        if not endpoints <= node_ids:
            raise ValueError("Unknown edge endpoint")
        key = (edge["from"], edge["to"], edge["relation"], edge["detail"])
        if key in seen or not edge["detail"].strip():
            raise ValueError("Duplicate edge or empty detail")
        seen.add(key)
        if edge["status"] == "source-backed" and edge["relation"] in RELATIONS:
            if endpoints & hypotheses:
                raise ValueError("Source-backed edge touches a hypothetical node")
            validate_location(edge["evidence"], source_ids)
        elif (edge["status"], edge["relation"]) == ("inferred", "possible-connection"):
            if "evidence" in edge or edge["to"] not in hypotheses:
                raise ValueError("Inferred edge must point to a hypothetical node without evidence")
        else:
            raise ValueError("Invalid edge status or relation")


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_sources(sources):
    if any(not 0 < source["bytes"] <= MAX_FILE_BYTES for source in sources):
        raise ValueError("A pinned file exceeds the per-file byte budget")
    if sum(source["bytes"] + 1 for source in sources) > MAX_TOTAL_BYTES:
        raise ValueError("The allowlist exceeds the aggregate byte budget")
    opener = build_opener(NoRedirects)
    files = {}
    for source in sources:
        with opener.open(source["raw_url"], timeout=15) as response:
            body = response.read(source["bytes"] + 1)
        if len(body) != source["bytes"] or hashlib.sha256(body).hexdigest() != source["sha256"]:
            raise ValueError(f"Byte length or SHA-256 mismatch for {source['path']}")
        files[source["id"]] = body.decode("utf-8").splitlines()
        print(f"{source['sha256']}  {source['bytes']:>6}  {source['path']}")
    return files


def check_anchors(registry, files):
    for item in registry["nodes"] + registry["edges"]:
        if "evidence" not in item:
            continue
        evidence = item["evidence"]
        first, last = evidence["lines"]
        lines = files[evidence["source_id"]]
        snippet = "\n".join(lines[first - 1:last])
        if last > len(lines) or evidence["anchor"] not in snippet:
            raise ValueError(f"Missing anchor at {evidence['source_id']}:{first}-{last}: {evidence['anchor']}")

    handoff = files["handoff"]
    if "\n".join(handoff[68:71]).removesuffix(" :=") != HANDOFF_SIGNATURE:
        raise ValueError("Handoff signature differs from the audited source")
    extraction = (ROOT / "lean/extraction/Extraction/LogSquare.lean").read_text(encoding="utf-8")
    signature = "\n".join(files["divisibility"][58:60]).removesuffix(" := by")
    if signature + " := by\n" not in extraction:
        raise ValueError("Logarithm estimate signature differs from the audited source")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Regenerate the receipt after all source checks")
    parser.add_argument("--offline", action="store_true", help="Validate the existing receipt without HTTP")
    args = parser.parse_args()
    if args.offline and args.write:
        parser.error("--offline cannot be combined with --write")
    try:
        registry = build_registry()
        validate_registry(registry)
        if not args.offline:
            check_anchors(registry, fetch_sources(registry["sources"]))
        rendered = json.dumps(registry, ensure_ascii=False, indent=2) + "\n"
        if args.write:
            RECEIPT.write_text(rendered, encoding="utf-8", newline="\n")
        elif RECEIPT.read_text(encoding="utf-8") != rendered:
            raise ValueError("Receipt differs from the curated registry; run with --write")
    except (ValueError, OSError, URLError) as error:
        parser.exit(1, f"Arithmetic handoff check failed: {error}\n")
    mode = "offline receipt" if args.offline else "source pins, anchors, and receipt"
    print(f"Checked {mode} for {len(registry['sources'])} files, "
          f"{len(registry['nodes'])} nodes and {len(registry['edges'])} edges.")


if __name__ == "__main__":
    main()
