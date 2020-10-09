import pandas as pd
import pickle

def parse(df, domain_to_insti, history):
    """Returns an openreview dataset after matching institution to author"""
    
    def parse(row):
        if not isinstance(row['emails'], str):
            return ""
        emails = row['emails'].split(";")
        if isinstance(row['submission_date'], str):
            year = int("20" + str(row['submission_date'].split("/")[2]))
        else:
            year = row['year']
        institutions = []
        for email in emails:
            found = False
            
            # check if domain in email is in domain_to_insti
            for domain in domain_to_insti.keys():
                if domain in email:
                    institutions.append(domain_to_insti[domain])
                    found = True
                    break
            if found:
                continue
                
            # if not, look into openreview profile data
            if email in history:
                for period in history[email]:
                    start, end, domain, institution = period[0], period[1], period[2], period[3]
                    if (start == -1 or year >= start) and (end == -1 or year <= end):
                        if domain in domain_to_insti:    
                            institutions.append(domain_to_insti[domain])
                            found = True
                            break
                        for key in domain_to_insti.keys():
                            if key in domain:
                                institutions.append(domain_to_insti[key])
                                found = True
                                break
                        if found:
                            break
                        institutions.append(institution)
                        found = True
                        break
            if found:
                continue
                
            # if not, check if the email has ".com" in the tail
            if isinstance(email, str) and len(email.split("@")) <= 1:
                continue
            domain = email.split("@")[1]
            if domain not in email_services and ".com" in domain:
                institutions.append(domain.replace(".com", "").capitalize())
                found = True
            if not found:
                institutions.append("")
        
        return ';'.join(institutions)
        
    ans = df.copy()
    ans['institution'] = ans.apply(parse, axis = 1)
    return ans

if __name__ == "__main__":
    domain_to_insti, history = None, None

    with open("domain_to_insti.p", 'rb') as fp:
        domain_to_insti = pickle.load(fp)
        
    with open("email_to_history.p", 'rb') as fp:
        history = pickle.load(fp)
        
    email_services = set(['gmail.com', 'yahoo.com','hotmail.com','aol.com', 'hotmail.co.uk', 'hotmail.fr',
                          'msn.com', 'yahoo.fr', 'wanadoo.fr', 'orange.fr', 'comcast.net', 'yahoo.co.uk',
                          'yahoo.com.br', 'yahoo.co.in', 'live.com', 'rediffmail.com', 'free.fr', 'gmx.de',
                          'web.de', 'yandex.ru', 'ymail.com', 'libero.it', 'outlook.com', 'uol.com.br',
                          'bol.com.br', 'mail.ru', 'cox.net', 'hotmail.it', 'sbcglobal.net', 'sfr.fr', 'live.fr',
                          'verizon.net', 'live.co.uk', 'googlemail.com', 'yahoo.es', 'ig.com.br', 'live.nl',
                          'bigpond.com', 'terra.com.br', 'yahoo.it', 'neuf.fr', 'yahoo.de', 'alice.it',
                          'rocketmail.com', 'att.net', 'laposte.net', 'facebook.com', 'bellsouth.net', 'yahoo.in',
                          'hotmail.es', 'charter.net', 'yahoo.ca', 'yahoo.com.au', 'rambler.ru', 'hotmail.de',
                          'tiscali.it', 'shaw.ca', 'yahoo.co.jp', 'sky.com', 'earthlink.net', 'optonline.net',
                          'freenet.de', 't-online.de', 'aliceadsl.fr', 'virgilio.it', 'home.nl', 'qq.com',
                          'telenet.be', 'me.com', 'yahoo.com.ar', 'tiscali.co.uk', 'yahoo.com.mx', 'voila.fr',
                          'gmx.net', 'mail.com', 'planet.nl', 'tin.it', 'live.it', 'ntlworld.com', 'arcor.de',
                          'yahoo.co.id', 'frontiernet.net', 'hetnet.nl', 'live.com.au', 'yahoo.com.sg', 'zonnet.nl',
                          'club-internet.fr', 'juno.com', 'optusnet.com.au', 'blueyonder.co.uk', 'bluewin.ch',
                          'skynet.be', 'sympatico.ca', 'windstream.net',
                          'mac.com', 'centurytel.net', 'chello.nl', 'live.ca', 'aim.com', 'bigpond.net.au'])
    
    df = pd.read_csv("openreview.csv", quotechar = '"')
    new_df = parse(df, domain_to_insti, history)
    new_df.to_csv("openreview.csv", encoding='utf-8', index=False)
