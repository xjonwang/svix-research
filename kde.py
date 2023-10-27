import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

data = np.random.randn(1000)
kde = gaussian_kde(data)

def custom_pdf(kde, x):
    return kde.evaluate(x)

def generate_samples(kde, n):
    return kde.resample(size=n)
    
n_samples = 1000
samples = generate_samples(kde, n_samples)
xrange = np.linspace(min(data), max(data), 1000)

print(data)
print(samples[0])
print(type(data), type(samples))
plt.figure(figsize=(12, 6))
plt.hist(data, bins=30, density=True, alpha=0.4, color='g', label='Original Data')
plt.hist(samples[0], bins=30, density=True, alpha=0.4, color='r', label='Sampled Data')
plt.plot(xrange, kde(xrange), color='k', label='KDE')
plt.legend()
plt.title('Sampling from a PDF based on KDE')
plt.show()