
using System;
using MonteCarloOptionPricer.Models;
using MonteCarloOptionPricer.Simulation;
using MonteCarloOptionPricer.Pricing;
using MonteCarloOptionPricer.Greeks;

namespace MonteCarloOptionPricer
{
    class Program
    {
        static void Main(string[] args)
        {
            // Prompt for initial asset price (S0)
            double s0 = ReadDouble("Enter the initial asset price (S0):", 100.0);

            // Prompt for strike price (K)
            double k = ReadDouble("Enter the strike price (K):", 100.0);

            // Prompt for volatility (e.g., 0.2 for 20%)
            double volatility = ReadDouble("Enter the volatility (e.g., 0.2 for 20%):", 0.2);

            // Prompt for risk-free rate (e.g., 0.05 for 5%)
            double riskFreeRate = ReadDouble("Enter the risk-free rate (e.g., 0.05 for 5%):", 0.05);

            // Prompt for time to maturity in years (T)
            double maturity = ReadDouble("Enter the time to maturity in years (T):", 1.0);

            // Prompt for the number of simulation paths
            int numberOfPaths = ReadInt("Enter the number of simulation paths:", 100000);

            // Prompt for the number of time steps per simulation path
            int timeSteps = ReadInt("Enter the number of time steps per simulation path:", 100);

            // Prompt for the option type (C for Call, P for Put)
            bool isCall = ReadOptionType("Enter the option type (C for Call, P for Put):", true);


            // Create the PricingParameters object using the validated inputs
            var parameters = new PricingParameters(
                s0: s0,
                k: k,
                volatility: volatility,
                riskFreeRate: riskFreeRate,
                maturity: maturity,
                numberOfPaths: numberOfPaths,
                timeSteps: timeSteps,
                isCall: isCall
            );

            Console.WriteLine("Enter the option style (E for European, A for American):");
            string? styleInput = Console.ReadLine();
            bool isAmerican = styleInput?.Trim().ToUpper() == "A";



            double optionPrice;

            if (!isAmerican)
                {
                    // Prompt to see if they want the Greeks returned as well (Y for yes, N for no)
                    bool isGreeks = ReadBool("Would you like to see the option Greeks as well? (Y for yes, N for no)", true);


                    // -- European Logic --
                    var simulator = new MonteCarloSimulator();
                    var finalPrices = simulator.SimulateFinalPrices(parameters);

                    var pricer = new EuropeanOptionPricer();
                    optionPrice = pricer.PriceOption(parameters, finalPrices);

                    Console.WriteLine();
                    Console.WriteLine($"(European) {(parameters.IsCall ? "Call" : "Put")} Option Price: {optionPrice:F4}");

                    if (isGreeks)
                    {

                        double baselinePrice = optionPrice;  
                        
                        // Instantiate the Greeks estimator
                        var greeksEstimator = new MonteCarloOptionPricer.Greeks.MonteCarloGreeksEstimator();

                        // Estimate Greeks
                        double delta = greeksEstimator.EstimateDelta(parameters, baselinePrice);
                        double vega = greeksEstimator.EstimateVega(parameters, baselinePrice);
                        double theta = greeksEstimator.EstimateTheta(parameters, baselinePrice);
                        double rho = greeksEstimator.EstimateRho(parameters, baselinePrice);
                        double gamma = greeksEstimator.EstimateGamma(parameters, baselinePrice);
                        Console.WriteLine();
                        Console.WriteLine("=== Greeks ===");
                        Console.WriteLine($"Delta: {delta:F4}");
                        Console.WriteLine($"Vega:  {vega:F4}");
                        Console.WriteLine($"Theta: {theta:F4}");
                        Console.WriteLine($"Rho:   {rho:F4}"); 
                        Console.WriteLine($"Gamma: {gamma:F4}");
                    }
                }
                else
                {
                    // -- American Logic (LSM) --
                    var simulator = new MonteCarloSimulator();
                    var assetPaths = simulator.SimulateAssetPaths(parameters);

                    var americanPricer = new AmericanOptionPricer();
                    optionPrice = americanPricer.PriceAmericanOption(parameters, assetPaths);

                    Console.WriteLine();
                    Console.WriteLine($"(American) {(parameters.IsCall ? "Call" : "Put")} Option Price: {optionPrice:F4}");
                }

            
            // Run the Monte Carlo simulation and option pricing
            // var simulator = new MonteCarloSimulator();
            // var finalPrices = simulator.SimulateFinalPricesAntithetic(parameters);

            // var pricer = new EuropeanOptionPricer();
            // double optionPrice = pricer.PriceOption(parameters, finalPrices);

             
            
        }

        // Helper method to read a double with validation and a default value
        static double ReadDouble(string prompt, double defaultValue)
        {
            while (true)
            {
                Console.WriteLine(prompt);
                string? input = Console.ReadLine();

                // If input is null or whitespace, use the default value
                if (string.IsNullOrWhiteSpace(input))
                {
                    Console.WriteLine($"No input detected. Defaulting to {defaultValue}.");
                    return defaultValue;
                }

                if (double.TryParse(input, out double result))
                {
                    return result;
                }
                else
                {
                    Console.WriteLine("Invalid input. Please enter a numeric value.");
                }
            }
        }

        // Helper method to read an integer with validation and a default value
        static int ReadInt(string prompt, int defaultValue)
        {
            while (true)
            {
                Console.WriteLine(prompt);
                string? input = Console.ReadLine();

                if (string.IsNullOrWhiteSpace(input))
                {
                    Console.WriteLine($"No input detected. Defaulting to {defaultValue}.");
                    return defaultValue;
                }

                if (int.TryParse(input, out int result))
                {
                    return result;
                }
                else
                {
                    Console.WriteLine("Invalid input. Please enter an integer value.");
                }
            }
        }

        // Helper method to read the option type and return true for Call and false for Put.
        static bool ReadOptionType(string prompt, bool defaultIsCall)
        {
            while (true)
            {
                Console.WriteLine(prompt);
                string? input = Console.ReadLine();

                // Default if no input is provided
                if (string.IsNullOrWhiteSpace(input))
                {
                    Console.WriteLine($"No input detected. Defaulting to {(defaultIsCall ? "Call" : "Put")}.");
                    return defaultIsCall;
                }

                input = input.Trim().ToUpper();
                if (input == "C")
                {
                    return true;
                }
                else if (input == "P")
                {
                    return false;
                }
                else
                {
                    Console.WriteLine("Invalid input. Please type 'C' for Call or 'P' for Put.");
                }

            }
        }

        static bool ReadBool(string prompt, bool True)
        {
            while (true)
            {
                Console.WriteLine(prompt);
                string? input = Console.ReadLine();

                if (string.IsNullOrWhiteSpace(input))
                {
                    Console.WriteLine($"No input detected. Defaulting to Yes.");
                    return true;
                }

                input = input.Trim().ToUpper();
                if (input == "Y")
                {
                    return true;
                }
                else if (input == "N")
                {
                    return false;
                }
                else
                {
                    Console.WriteLine("Invalid input. Please type 'Y' for yes or 'N' for No.");
                }


            }
        }
    }
}

