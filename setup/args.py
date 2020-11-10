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

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()
