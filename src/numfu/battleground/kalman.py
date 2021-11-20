# a simple kalman filter

# state matrix:             2N+1 values
# 
#  x, y, vx, vy, ax, ay, ...
#
#
# measurement matrix:      2N+1 values
#
#  x, y
#

class KalmanFilter:

    def __init__(self, dt, u, std_acc, std_meas):
        # dt - time step

        self.dt = dt
        self.u = u
        self.std_acc = std_acc
        self.std_meas = std_meas

        # intial guesses
        self.X = np.matrix([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]).T
        self.P = np.matrix([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 1000.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 1000.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 1000.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 1000.0]])

        self.F = np.matrix([[1.0, 0.0, dt, 0.0, (dt**2)/2, 0.0],
                            [0.0, 1.0, 0.0, dt, 0.0, (dt**2)/2],
                            [0.0, 0.0, 1.0, 0.0, dt, 0.0],
                            [0.0, 0.0, 0.0, 1.0, 0.0, dt],
                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])

        self.H = np.matrix([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0]])

        self.R = np.matrix([[std_meas**2, 0.0],
                            [0.0, std_meas**2]])

        self.I = np.eye(self.X.shape[0])

    def predict(self):
        self.X = self.F * self.X
        self.P = self.F * self.P * self.F.T + self.Q

    def measure(self, z):
        K = self.P * self.H.T * np.linalg.inv(self.H * self.P * self.H.T + self.R)
        self.X = self.X + K * (z - self.H * self.X)
        self.P = (self.I - K * self.H) * self.P

    def measure_and_update(self, z):
        self.predict()
        self.measure(z)

    def set_Q(self, q):
        self.Q = np.matrix([[q, 0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, q, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 0.0, q, 0.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, q, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 0.0, q, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, q]])

    def set_R(self, r):
        self.R = np.matrix([[r, 0.0],
                            [0.0, r]])


def main():
    dt = 0.1
    std_acc = 0.1
    std_meas = 0.1

    u = np.matrix([[0.0],
                   [0.0],
                   [0.0],
                   [0.0],
                   [0.0],
                   [0.0]])

    kf = KalmanFilter(dt, u, std_acc, std_meas)

    zs = []
    kalman_predictions = []
    for i in range(100):
        z = np.matrix([[i+randn()*std_meas],
                       [i+randn()*std_meas]])
        zs.append(z)

        kf.measure_and_update(z)

        kalman_prediction = kf.X
        kalman_predictions.append(np.array(kalman_prediction).flatten())

    kalman_predictions = np.array(kalman_predictions)

    for z, kalman_prediction in zip(zs, kalman_predictions):
        print('z:      ', z.T)
        print('pred:   ', kalman_prediction)
        print()


if __name__ == '__main__':
    main()