using System;

namespace MonteCarloOptionPricer.Models
{
    public class PricingParameters
    {
        // Underlying Price
        public double S0 { get; set; }

        // Strike
        public double K { get; set; }

        // Volatility
        public double Volatility { get; set; }

        // Risk-free rate
        public double RiskFreeRate { get; set; }

        // Time to maturity 
        public double Maturity { get; set; }

        // Number of Monte Carlo simulation paths
        public int NumberOfPaths { get; set; }

        // Number of time steps in each simulation path
        public int TimeSteps { get; set; }

        // Is it a call or put 
        public bool IsCall { get; set; }


        // Constructor
        public PricingParameters(double s0, double k, double volatility, double riskFreeRate, 
                                double maturity, int numberOfPaths, int timeSteps, bool isCall)
        {
            {
            S0 = s0;
            K = k;
            Volatility = volatility;
            RiskFreeRate = riskFreeRate;
            Maturity = maturity;
            NumberOfPaths = numberOfPaths;
            TimeSteps = timeSteps;
            IsCall = isCall;
        }


    }

}
}