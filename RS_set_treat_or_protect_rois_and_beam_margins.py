""" Python code example: Set treat or protect rois and beam margins """
from connect import get_current

def set_treat_or_protect_rois_and_beam_margins(roi_name, beam_no):
    """ Set treat or protect rois and beam margins """

    beam_set = get_current('BeamSet')

    beam = beam_set.Beams[beam_no]

    # Set the ROI as a Treat or Protect ROI for the beam
    beam.SetTreatOrProtectRoi(RoiName = roi_name)

    # Set beam margins for the beam
    beam.SetTreatAndProtectMarginsForBeam(TopMargin = 0, BottomMargin = 0, LeftMargin = 1, RightMargin = 1, Roi = roi_name)

if __name__ == '__main__':
    set_treat_or_protect_rois_and_beam_margins('SpinalCord', 0)
