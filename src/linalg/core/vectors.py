import numpy as np

a = np.array([2, -1, 3])
b = np.array([1, 4, -2])

print(a + b)                  # [3 3 1]
print(a - b)                  # [ 1 -5  5]
print(3 * a)                  # [ 6 -3  9]
print(a @ b)                  # -8  (dot product)
print(a * b)                  # [ 2 -4 -6]  <- element-wise, NOT a dot product

norm_a = np.linalg.norm(a)    # 3.7416...
unit_a = a / norm_a

cos_theta = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
theta = np.degrees(np.arccos(cos_theta))
print(theta)                  # ~117.8
