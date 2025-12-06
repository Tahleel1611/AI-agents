#!/usr/bin/env python3
"""
SmartTravel AI - Main Entry Point
Multi-agent travel concierge CLI application
"""

import sys
import argparse
import logging
from pathlib import Path

# Add smarttravel to path
sys.path.insert(0, str(Path(__file__).parent / 'smarttravel'))

from smarttravel.agents.concierge import TravelConcierge


def setup_logging(verbose: bool = False):
    """Configure logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    """Main CLI entrypoint for SmartTravel AI."""
    parser = argparse.ArgumentParser(
        description='SmartTravel AI - Your intelligent travel planning assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py "Plan a 5-day trip to Paris for 2 people"
  python main.py -v "Find hotels in Tokyo under $150/night"
  python main.py --interactive
        '''
    )
    
    parser.add_argument(
        'query',
        nargs='?',
        help='Your travel planning query'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize concierge
        logger.info("Initializing SmartTravel AI Concierge...")
        concierge = TravelConcierge()
        
        if args.interactive:
            # Interactive mode
            logger.info("Starting interactive mode. Type 'quit' or 'exit' to stop.")
            print("\n🤖 SmartTravel AI - Interactive Mode")
            print("=" * 50)
            print("Type your travel queries or 'quit' to exit.\n")
            
            while True:
                try:
                    user_input = input("You: ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        print("\nThank you for using SmartTravel AI! Safe travels! ✈️")
                        break
                    
                    if not user_input:
                        continue
                    
                    # Process query
                    response = concierge.process_request(user_input)
                    print(f"\n🤖 Assistant: {response}\n")
                    
                except KeyboardInterrupt:
                    print("\n\nInterrupted. Exiting...")
                    break
                    
        elif args.query:
            # Single query mode
            logger.info(f"Processing query: {args.query}")
            print(f"\n🤖 SmartTravel AI")
            print("=" * 50)
            
            response = concierge.process_request(args.query)
            print(f"\n{response}\n")
            
        else:
            # No arguments provided
            parser.print_help()
            return 1
            
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=args.verbose)
        print(f"\n❌ An error occurred: {str(e)}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
