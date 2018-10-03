# -*- coding: utf-8 -*-

# Vutils for Math

import math
import numpy as NP

# ---

def LinearRegression(Xs, Ys):

    #  Fx = βx + α

    #  Fx = βx                                   # suppose α = 0 for simplicity

    #  J  = ∑(F𝗑ᵢ - yᵢ)² = ∑((α + β*xᵢ) - yᵢ)²      # the function J called the cost/lost function

    #  J  = ∑(F𝗑ᵢ - yᵢ)² = ∑(βxᵢ - yᵢ)² = ∑(β²xᵢ² - 2βxᵢyᵢ - y²)

    #  J' = ∑(2βxᵢ² - 2xᵢyᵢ) = ∑2βxᵢ² - ∑2xᵢyᵢ       # derivatives J to find the slope

    # ½J' = ∑βxᵢ² - ∑xᵢyᵢ

    # ½J' = 0 <=> ∑βxᵢ² - ∑xᵢyᵢ = 0                # finding the slope of J

    # β   = ∑xᵢyᵢ ÷ ∑xᵢ²

    # α   = Fxᵢ - βxᵢ (xᵢ & yᵢ here are mean of x & y)

    nPairs = min(NP.size(Xs), NP.size(Ys)) # pairs of data

    meanX, meanY = NP.mean(Xs), NP.mean(Ys)

    totalXY = totalXX = 0.

    for i in xrange(0, nPairs):
        totalXY += (Xs[i] - meanX) * (Ys[i] - meanY)  # ∑xᵢyᵢ
        totalXX += (Xs[i] - meanX) * (Xs[i] - meanX)  # ∑xᵢ²
    pass

    B = totalXY / totalXX   # β = ∑xᵢyᵢ ÷ ∑xᵢ²
    A = meanY - B * meanX   # α = Fxᵢ - βxᵢ (xᵢ & yᵢ here are mean of x & y)

    return (A, B)   # α & β

# ---

def Angle2D(P1, P2):
    X1, Y1 = P1
    X2, Y2 = P2
    a = (Y2 - Y1)
    b = (X2 - X1)
    return math.degrees(math.atan2(b, a))

def Distance2D(P1, P2) :
    X1, Y1 = P1
    X2, Y2 = P2
    return math.sqrt((X2 - X1)**2 + (Y2 - Y1)**2)