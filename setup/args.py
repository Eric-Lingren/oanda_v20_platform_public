import argparse

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Oanda v20 API integration')

    parser.add_argument('--account', default=None,
                        required=True, action='store',
                        help='Account identifier to use')
    
    # parser.add_argument('--compression', default=1, type=int,
    #                     required=False, action='store',
    #                     help='Compression for Resample/Replay')

    parser.add_argument('--pair', default=None,
                        required=True, action='store',
                        help='data 0 into the system')
    
    parser.add_argument('--live', default=None,
                        required=False, action='store',
                        help='Go to live server rather than practice')
    
    # parser.add_argument('--timeframe', default=TIMEFRAMES[2],
    #                     choices=TIMEFRAMES,
    #                     required=False, action='store',
    #                     help='TimeFrame for Resample/Replay')
    
    parser.add_argument('--token', default=None,
                        required=True, action='store',
                        help='Access token to use')
    
    parser.add_argument('--twilio-number', default=None,
                        required=False, action='store',
                        help='Twilio number to send mesages from')
    
        
    parser.add_argument('--recipient-number', default=None,
                        required=False, action='store',
                        help='Number to send mesages to')
    
    parser.add_argument('--bot', default=None,
                        required=True, action='store',
                        help='System bot to trade')
    
    parser.add_argument('--twilio-sid', default=None,
                        required=False, action='store',
                        help='Twilio account')
    
    parser.add_argument('--twilio-token', default=None,
                        required=False, action='store',
                        help='Twilio auth account')


    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()
