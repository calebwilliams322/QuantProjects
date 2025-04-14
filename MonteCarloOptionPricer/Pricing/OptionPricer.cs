using System;
using System.Collections.Generic;
using MonteCarloOptionPricer.Models;
using MathNet.Numerics.LinearAlgebra;
using MathNet.Numerics.LinearAlgebra.Double;


namespace MonteCarloOptionPricer.Pricing
{
    public class EuropeanOptionPricer 
    {
        /// Prices a European Option using monte carlo results
        /// Completely decoupled from the simulation engine
        /// <param name="parameters">The pricing parameters.</param>
        /// <param name="finalPrices">A list of simulated terminal asset prices.</param>
        /// <returns>The estimated option price.</returns>
        
        public double PriceOption(PricingParameters parameters, List<double> finalPrices)
        {
            double sumPayoffs = 0.0;

            // loop through all of the final asset prices 
            foreach (var S_T in finalPrices)
            {

                if (parameters.IsCall)
                {
                    // Call option payoff: max(S_T - K, 0)
                    sumPayoffs += Math.Max(S_T - parameters.K, 0.0);
                }
                else
                {
                    // Put option payoff: max(K - S_T, 0)
                    sumPayoffs += Math.Max(parameters.K - S_T, 0.0);
                }

            }
            double averagePayoff = sumPayoffs / finalPrices.Count;

            return Math.Exp(-parameters.RiskFreeRate * parameters.Maturity) * averagePayoff;
        }
    }

    public class AmericanOptionPricer
    {

        /// Prices an American option using the Least Squares Monte Carlo (LSM) approach
        /// Assumes assetPath is a list of double arrays where each array is a path
        /// <param name="parameters">The pricing parameters.</param>
        /// <param name="assetPaths">=The matrix of asset paths.</param>
        /// <returns> The estimated option price. <returns>
        

        public double PriceAmericanOption(PricingParameters parameters, List<double[]> assetPaths)
        {
            int nPaths = assetPaths.Count;
            int nSteps = parameters.TimeSteps;
            double deltaT = parameters.Maturity / parameters.TimeSteps;

            // initialize array that holds cash flows
            double[] cashFlows = new double[nPaths];

            // Initialize all of the cash flows at each point
            for (int i = 0; i < nPaths; i++)
            {
                double ST = assetPaths[i][nSteps];
                cashFlows[i] = ImmediatePayoff(ST, parameters);

            }

            // Backwards Induction
            for (int step = nSteps - 1; step >= 1; step--)
            {
                var regressionData = new List<(double S, double Y, int PathIndex)>();


                for (int i = 0; i < nPaths; i++)
                {
                    double S = assetPaths[i][step];
                    double immediatePay = ImmediatePayoff(S, parameters);

                    // Only consider in-the-money paths 
                    if (immediatePay > 0)
                    {
                        // Discount the cash flow from the next time step to time step 'step'.
                        double discountedCF = cashFlows[i] * Math.Exp(-parameters.RiskFreeRate * deltaT);
                        regressionData.Add((S, discountedCF, i));
                    }
                }

                // If we have in the money paths we must perform regression
                double[]? beta = null;
                if (regressionData.Count > 0)
                {
                    int m = regressionData.Count;
                    double[,] X = new double[m, 3];
                    double[] Y = new double[m];
                    
                    for (int j = 0; j < m; j++)
                    {
                        double S = regressionData[j].S;
                        X[j, 0] = 1.0;
                        X[j, 1] = S;
                        X[j, 2] = S * S;
                        Y[j] = regressionData[j].Y;
                    }
                    
                    // Calculate beta coefficients via ordinary least squares.
                    beta = OLSRegression(X, Y);
                }

                if (beta != null)
                {
                    foreach (var data in regressionData)
                    {
                        double S = data.S;
                        double exerciseValue = ImmediatePayoff(S, parameters);
                        double continuationValue = beta[0] + beta[1] * S + beta[2] * S * S;
                        
                        if (exerciseValue > continuationValue)
                        {
                            // Update cash flow for the path if exercising is optimal.
                            cashFlows[data.PathIndex] = exerciseValue;
                        }
                    }
                }
                else
                {
                    // If no paths are in-the-money, nothing to update for this step.
                }

            }

            double priceSum = 0;
            for (int i = 0; i < nPaths; i++)
            {
                priceSum += cashFlows[i] * Math.Exp(-parameters.RiskFreeRate * deltaT);
            }
            
            return priceSum / nPaths;

        }


       
        // Helper function do compute the immediate payoff
        private double ImmediatePayoff(double stockPrice, PricingParameters parameters)
        {
            if (parameters.IsCall)
                return Math.Max(stockPrice - parameters.K, 0);
            else
                return Math.Max(parameters.K - stockPrice, 0);
        }

        
        private double[] OLSRegression(double[,] X, double[] Y)
        {
            // Convert X and Y to Math.NET structures.
            var XMatrix = DenseMatrix.OfArray(X);
            var YVector = DenseVector.OfArray(Y);

            // Compute the pseudo-inverse of X.
            // The pseudo-inverse is more robust than directly inverting (X^T X)
            // for least squares problems.
            var pseudoInverse = XMatrix.PseudoInverse();

            // Compute beta coefficients: beta = pseudoInverse * Y
            var beta = pseudoInverse * YVector;

            return beta.ToArray();
        }
        

    }



}