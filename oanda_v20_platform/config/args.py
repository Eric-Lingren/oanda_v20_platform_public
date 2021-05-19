import argparse


def parse_args(pargs=None):
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Oanda v20 API integration')

    parser.add_argument('--bot', default='rsi_test',
                    required=True, action='store',
                    help='System bot to trade')

                        
    parser.add_argument('--pair', default='EUR_USD',
                        required=True, action='store',
                        help='data 0 into the system')
    
    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()

# %%
