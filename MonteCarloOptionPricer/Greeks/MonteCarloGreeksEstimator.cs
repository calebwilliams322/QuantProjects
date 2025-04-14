using System;
using MonteCarloOptionPricer.Models;
using MonteCarloOptionPricer.Simulation;
using MonteCarloOptionPricer.Pricing;


namespace MonteCarloOptionPricer.Greeks
{

    public class MonteCarloGreeksEstimator
    {

        // Here we will set the default perturbation values for our greeks esimation
        public double DeltaEpsilon {get; set;} = 0.1;
        public double VolatilityEpsilon {get; set;} = 0.1;
        public double TimeEpsilon {get; set;} = 0.1;
        public double RateEpsilon {get; set;} = 0.001;


        // Declare simulator and pricer instances
        private readonly Simulation.MonteCarloSimulator _simulator;
        private readonly Pricing.EuropeanOptionPricer _pricer;

        // Constructor

        public MonteCarloGreeksEstimator()
        {

            _simulator = new MonteCarloSimulator();
            _pricer = new EuropeanOptionPricer();

        }

        // We should have an option pricer helper function that uses the OptionPricer class

        private double PriceOption(PricingParameters parameters)
        {
            // Get the final payoffs by simulation
            var finalPayoffs = _simulator.SimulateFinalPrices(parameters);
            // Use functionality of _pricer object
            return _pricer.PriceOption(parameters, finalPayoffs);
        }

        // Now we can begin creating the methods for estimating greeks
        public double EstimateDelta(PricingParameters parameters, double originalPrice)
        {
            double originalS0 = parameters.S0;
            double epsilon = DeltaEpsilon;
            parameters.S0 = originalS0 + epsilon;

            // run simulation with new underlying price
            double pricePlus = PriceOption(parameters);

            // place the old price back
            parameters.S0 = originalS0;

            // calculate delta
            double delta = (pricePlus - originalPrice) / epsilon;
            return delta;

        }

        public double EstimateVega(PricingParameters parameters, double originalPrice)
        {
        
            double originalVol = parameters.Volatility;
            double epsilon = VolatilityEpsilon;
            
            // Perturb the volatility upward.
            parameters.Volatility = originalVol + epsilon;
            double pricePlus = PriceOption(parameters);
            
            // Restore the original volatility.
            parameters.Volatility = originalVol;
            
            return (pricePlus - originalPrice) / epsilon;
        }

        public double EstimateTheta(PricingParameters parameters, double baselinePrice)
        {
            double originalMaturity = parameters.Maturity;
            double epsilon = TimeEpsilon;
            
            // Perturb the time to maturity upward.
            parameters.Maturity = originalMaturity + epsilon;
            double pricePlus = PriceOption(parameters);
            
            // Restore the original maturity.
            parameters.Maturity = originalMaturity;
            
            // The negative sign reflects that Theta is the negative derivative with respect to time.
            return -(pricePlus - baselinePrice) / epsilon;
        }

        public double EstimateRho(PricingParameters parameters, double baselinePrice)
        {
            double originalRate = parameters.RiskFreeRate;
            double epsilon = RateEpsilon;
            
            // Perturb the risk-free rate upward.
            parameters.RiskFreeRate = originalRate + epsilon;
            double pricePlus = PriceOption(parameters);
            
            // Restore the original risk-free rate.
            parameters.RiskFreeRate = originalRate;
            
            return (pricePlus - baselinePrice) / epsilon;
        }

        public double EstimateGamma(PricingParameters parameters, double baselinePrice)
        {
            double originalS0 = parameters.S0;
            double epsilon = DeltaEpsilon;

            parameters.S0 = originalS0 + epsilon;
            double pricePlus = PriceOption(parameters);
            
            // Price at S0 (baseline)
            parameters.S0 = originalS0;
            double price = PriceOption(parameters);
            
            // Price at S0 - epsilon
            parameters.S0 = originalS0 - epsilon;
            double priceMinus = PriceOption(parameters);

            // Reset S0
            parameters.S0 = originalS0;

            // Estimate Gamma
            return (pricePlus - 2 * price + priceMinus) / (epsilon * epsilon);
        }


        


    }

}