import cProfile

from auxiliary.nifti.io import read_nifti
from auxiliary.turbopath import turbopath

from panoptica import MatchedInstancePair, Panoptic_Evaluator
from panoptica.metrics import Metric

directory = turbopath(__file__).parent

ref_masks = read_nifti(directory + "/spine_seg/matched_instance/ref.nii.gz")

pred_masks = read_nifti(directory + "/spine_seg/matched_instance/pred.nii.gz")

sample = MatchedInstancePair(prediction_arr=pred_masks, reference_arr=ref_masks)


evaluator = Panoptic_Evaluator(
    expected_input=MatchedInstancePair,
    eval_metrics=[Metric.DSC, Metric.IOU],
    decision_metric=Metric.DSC,
    decision_threshold=0.5,
)


with cProfile.Profile() as pr:
    if __name__ == "__main__":
        result, debug_data = evaluator.evaluate(sample, verbose=True)
        print(result)

    pr.dump_stats(directory + "/instance_example.log")
