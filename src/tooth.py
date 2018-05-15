class Tooth():

    def __init__(self, landmarks):
        self.landmarks = landmarks

    def downscale(self, scale):
        self.landmarks *= scale

    def getLandmarks(self):
        return self.landmarks
