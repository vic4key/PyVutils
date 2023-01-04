# -*- coding: utf-8 -*-

# Vutils for Math

import math
import numpy as np

# ---

def linear_regression(xs, ys):

    # Fx  = βx + α
    # Fx  = βx                                                   # suppose α = 0 for simplicity
    # J   = ∑(F𝗑ᵢ - yᵢ)² = ∑((α + β*xᵢ) - yᵢ)²                   # the function J called the cost/lost function
    # J   = ∑(F𝗑ᵢ - yᵢ)² = ∑(βxᵢ - yᵢ)² = ∑(β²xᵢ² - 2βxᵢyᵢ - y²)
    # J'  = ∑(2βxᵢ² - 2xᵢyᵢ) = ∑2βxᵢ² - ∑2xᵢyᵢ                   # derivatives J to find the slope
    # ½J' = ∑βxᵢ² - ∑xᵢyᵢ
    # ½J' = 0 <=> ∑βxᵢ² - ∑xᵢyᵢ = 0                              # finding the slope of J
    # β   = ∑xᵢyᵢ ÷ ∑xᵢ²
    # α   = Fxᵢ - βxᵢ (xᵢ & yᵢ here are mean of x & y)

    num_pairs = min(np.size(xs), np.size(ys)) # pairs of data

    mean_x, mean_y = np.mean(xs), np.mean(ys)

    total_xy = total_xx = 0.

    for i in xrange(0, num_pairs):
        total_xy += (xs[i] - mean_x) * (ys[i] - mean_y)  # ∑xᵢyᵢ
        total_xx += (xs[i] - mean_x) * (xs[i] - mean_x)  # ∑xᵢ²
    pass

    b = total_xy / total_xx   # β = ∑xᵢyᵢ ÷ ∑xᵢ²
    a = mean_y - b * mean_x   # α = Fxᵢ - βxᵢ (xᵢ & yᵢ here are mean of x & y)

    return (a, b) # α & β
