import argparse
# import account details
from auth.auth import Tokens
t = Tokens()

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Oanda v20 API integration')

    # changed required from T to F for experiments running bot in vscode
    parser.add_argument('--bot', default=None,
                    required=False, action='store',
                    help='System bot to trade')

    # parser.add_argument('--compression', default=1, type=int,
    #                     required=False, action='store',
    #                     help='Compression for Resample/Replay')

    parser.add_argument('--email_to', default=None,
                    required=False, action='store',
                    help='The email address notifications will be sent to')
    
    parser.add_argument('--gmail_server_account', default=None,
                    required=False, action='store',
                    help='The email address notifications will be sent to')
    
    parser.add_argument('--gmail_server_password', default=None,
                    required=False, action='store',
                    help='The gmail application password for the senders acocunt')

    parser.add_argument('--live', default=None,
                        required=False, action='store',
                        help='Go to live server rather than practice')

    # changed required from T to F for experiments running bot in vscode
    parser.add_argument('--oanda_account', default=t.account,
                    required=False, action='store',
                    help='Oanda account identifier to use')

    # changed required from T to F for experiments running bot in vscode
    parser.add_argument('--oanda_token', default=t.token,
                        required=False, action='store',
                        help='Oanda API account access token to use')
                        
    # changed required from T to F for experiments running bot in vscode
    parser.add_argument('--pair', default=None,
                        required=False, action='store',
                        help='data 0 into the system')
    
    parser.add_argument('--recipient-number', default=None,
                        required=False, action='store',
                        help='Number to send mesages to')

    # parser.add_argument('--timeframe', default=TIMEFRAMES[2],
    #                     choices=TIMEFRAMES,
    #                     required=False, action='store',
    #                     help='TimeFrame for Resample/Replay')
    
    parser.add_argument('--twilio-number', default=None,
                        required=False, action='store',
                        help='Twilio number to send mesages from')

    parser.add_argument('--twilio-sid', default=None,
                        required=False, action='store',
                        help='Twilio account')
    
    parser.add_argument('--twilio-token', default=None,
                        required=False, action='store',
                        help='Twilio auth account')


    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args()
