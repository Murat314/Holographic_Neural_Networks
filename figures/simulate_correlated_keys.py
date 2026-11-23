"""Exploratory FHRR retrieval stress test with correlated keys.

Run: python figures/simulate_correlated_keys.py
The codebook comprises stored values only; each trial queries the first key.
Correlation is induced by phase deviations from a shared random anchor.
This does not model learned natural-language embeddings or a full LM.
"""
import numpy as np

D = 256
TRIALS = 500
LOADS = (8, 32, 64)
PHASE_STD = (0.3, 1.0, 3.0)
SEED = 2026


def experiment(dim, n, std, trials, rng):
    anchor = rng.uniform(-np.pi, np.pi, size=(trials, 1, dim))
    phase_keys = anchor + rng.normal(0, std, size=(trials, n, dim))
    keys = np.exp(1j * phase_keys).astype(np.complex64)
    values = np.exp(1j * rng.uniform(-np.pi, np.pi, size=(trials, n, dim))).astype(np.complex64)
    trace = np.sum(keys * values, axis=1)
    recalled = np.conj(keys[:, 0, :]) * trace
    scores = np.real(np.einsum('tnd,td->tn', np.conj(values), recalled, optimize=True)) / dim
    accuracy = float(np.mean(np.argmax(scores, axis=1) == 0))
    distractor_margin = float(np.mean(scores[:, 0] - np.max(scores[:, 1:], axis=1)))
    mean_key_similarity = float(np.mean(np.real(np.sum(np.conj(keys[:, 0]) * keys[:, 1], axis=1)) / dim))
    return mean_key_similarity, accuracy, distractor_margin


def main():
    rng = np.random.default_rng(SEED)
    print('D N phase_noise_std key_cos_similarity recall_top1 margin')
    for n in LOADS:
        for std in PHASE_STD:
            similarity, accuracy, margin = experiment(D, n, std, TRIALS, rng)
            print(f'{D} {n} {std:.2f} {similarity:.5f} {accuracy:.5f} {margin:.5f}')


if __name__ == '__main__':
    main()
