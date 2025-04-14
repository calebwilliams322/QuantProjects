using System;
using System.Collections.Generic;
using MonteCarloOptionPricer.Models;


namespace MonteCarloOptionPricer.Simulation
{

    public class MonteCarloSimulator
    {
        /// Generates ONLY the terminal asset prices for Euro Option using Monte Carlo
        /// <param name="parameters"> is an instance of the PricingParameters Class
        /// <returns> list of final simulated asset prices
        /// 
        
        public List<double> SimulateFinalPrices(PricingParameters parameters)
        {

            // New list the length of the number of paths
            var finalPrices = new List<double>(parameters.NumberOfPaths);

            // Find delta t
            double deltaT = parameters.Maturity / parameters.TimeSteps;


            // loop over number of paths
            for (int path = 0; path < parameters.NumberOfPaths; path++)
            {

                double S = parameters.S0;

                for (int step = 0; step < parameters.TimeSteps; step ++)
                {
                    // Get normal random from NormalGenerator
                    double z = NormalGenerator.NextStandardNormal();

                    // Geometric Brownian Motion equation
                    S *= Math.Exp((parameters.RiskFreeRate - 0.5 * Math.Pow(parameters.Volatility, 2)) * deltaT +
                        parameters.Volatility * Math.Sqrt(deltaT) * z);


                }

                finalPrices.Add(S);

            }

            return finalPrices;

        }

        public List<double> SimulateFinalPricesAntithetic(PricingParameters parameters)
        {
            // New list for simulated final prices.
            var finalPrices = new List<double>();

            double deltaT = parameters.Maturity / parameters.TimeSteps;

            // For each simulation, generate two paths with z and -z.
            // To keep the same number of independent draws, adjust the loop accordingly.
            for (int path = 0; path < parameters.NumberOfPaths; path++)
            {
                double s1 = parameters.S0;
                double s2 = parameters.S0; // For the antithetic path

                for (int step = 0; step < parameters.TimeSteps; step++)
                {
                    // Generate a standard normal variate.
                    double z = NormalGenerator.NextStandardNormal();
                    
                    // Update the asset price for the regular path using z.
                    s1 *= Math.Exp((parameters.RiskFreeRate - 0.5 * Math.Pow(parameters.Volatility, 2)) * deltaT
                                    + parameters.Volatility * Math.Sqrt(deltaT) * z);
                    // Update the asset price for the antithetic path using -z.
                    s2 *= Math.Exp((parameters.RiskFreeRate - 0.5 * Math.Pow(parameters.Volatility, 2)) * deltaT
                                    + parameters.Volatility * Math.Sqrt(deltaT) * (-z));
                }

                // Average the two terminal prices and add the result to the list.
                finalPrices.Add((s1 + s2) / 2.0);
            }

            return finalPrices;
        }


        public List<double> SimulateFinalPricesBoxMuller(PricingParameters parameters)
        {
            // New list for simulated final prices.
            var finalPrices = new List<double>();

            double deltaT = parameters.Maturity / (parameters.TimeSteps*2);

            // For each simulation, generate two paths with z and -z.
            // To keep the same number of independent draws, adjust the loop accordingly.
            for (int path = 0; path < parameters.NumberOfPaths; path++)
            {
                double S = parameters.S0;
               

                for (int step = 0; step < parameters.TimeSteps; step++)
                {
                    // Generate a standard normal variate.
                    var (z1, z2) = NormalGenerator.NextStandardNormalBothValues();
                    
                    // Update the asset price for the regular path using z.
                    S *= Math.Exp((parameters.RiskFreeRate - 0.5 * Math.Pow(parameters.Volatility, 2)) * deltaT
                                    + parameters.Volatility * Math.Sqrt(deltaT) * z1);

                    // 2) Then update S with z2
                    S *= Math.Exp(
                                    (parameters.RiskFreeRate - 0.5 * Math.Pow(parameters.Volatility, 2)) * deltaT
                                        + parameters.Volatility * Math.Sqrt(deltaT) * z2);
                }

                // Average the two terminal prices and add the result to the list.
                finalPrices.Add(S);
            }

            return finalPrices;
        }

        public List<double[]> SimulateAssetPaths(PricingParameters parameters)
        {
            /// A simulation that holds all asset paths and returns them as a matrix
            
            var assetPaths = new List<double[]>();
            double deltaT = parameters.Maturity / parameters.TimeSteps;

            for (int path = 0; path < parameters.NumberOfPaths; path++)
            {
                // Get asset prices for one path
                double[] prices = new double[parameters.TimeSteps + 1];
                prices[0] = parameters.S0;

                double S = parameters.S0;

                for (int step = 1; step <= parameters.TimeSteps; step++)
                {
                    // Grab random normal
                    double z = NormalGenerator.NextStandardNormal();

                    // Update S by one step
                    S *= Math.Exp((parameters.RiskFreeRate - 0.5 * Math.Pow(parameters.Volatility, 2))*deltaT 
                                    + parameters.Volatility * Math.Sqrt(deltaT) * z);

                    prices[step] = S;

                }
                assetPaths.Add(prices);

            }
            return assetPaths;
        }

            



        
     
    }

}