import numpy as np
import sys

from tracking.variables import *
from tracking.utils import save_pickle

class DataGenerator:
    """
    track is initialized at y = 0 and x = SIZE_LAYERS // 2. 
    Following a curved-tracjectory, the hit at each layer located at y = 1,...,NUMBER_LAYERS is given by
    x = x0 + charge * y**2 / (2*pT)

    charge [-1,+1] determine direction
    pT will be bounded by a pTmin assuring there is always a hit in last layer
    """

    def __init__(self, nTracks: int, ofile: str):
    
        self.x0 = SIZE_LAYERS // 2
        self.pTmin, self.pTmax = self.get_pt_bound()
        self.nTracks = nTracks
        if "." in ofile:
            raise ValueError("Please don't give file format name. Just write e.g. data/output")
        self.ofile = ofile

    def get_pt_bound(self):
        """
        we need | x(NUMBER_LAYERS) - x0 | < SIZE_LAYERS // 2
        """
        pTmin = NUMBER_LAYERS**2 / 2 / (SIZE_LAYERS // 2)
        pTmax = 5 * pTmin # This is just random...
        return pTmin, pTmax

    def generate_positions(self, pT: float, charge: int):
        return [
            int( self.x0 + charge * y**2 / (2 * pT) ) for y in range(1,NUMBER_LAYERS+1)
        ]
    
    def create_tracks(self):
        # We wanna pT to be closer to pTmax, not pTmin, so we generate the following:
        alpha = 0.8 # if alpha = 1, uniform distribution, while alpha -> 0 indicates strong preferance to pTmax
        u = np.random.rand(self.nTracks)
        pTs = self.pTmin + (u ** alpha) * (self.pTmax - self.pTmin)
        charges = np.random.choice([-1,+1], size=self.nTracks)

        self.tracks = []
        for pT, charge in zip(pTs, charges):
            self.tracks.append(
                (float(pT), int(charge), self.generate_positions(pT,charge))
            )

    def generate_data(self):
        self.create_tracks()
        save_pickle(self.ofile + "_truthTracks.pickle", self.tracks)
        
        self.hits = [
            [0] * SIZE_LAYERS for _ in range(NUMBER_LAYERS)
        ]
        for track in self.tracks:
            for i,hit in enumerate(track[-1]):
                self.hits[i][hit] += 1
        save_pickle(self.ofile + ".pickle", self.hits)


def main():

    if len(sys.argv) != 3:
        print("Please run python generate_data.py <nTracks> <ofile>")
        return
    
    nTracks = int(sys.argv[1])
    output = sys.argv[2]
    gen = DataGenerator(nTracks, output)
    gen.generate_data()
    
if __name__ == "__main__":
    main()