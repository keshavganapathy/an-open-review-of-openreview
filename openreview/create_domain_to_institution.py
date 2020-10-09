import pandas as pd
import pickle
    
def get_domain_to_insti_from_world_university(json):
    """Return a mapping from domain to the institution name from world university dataset"""
    domain_to_insti = dict()
    for name, domains in zip(list(json.name), list(json.domains)):
        for domain in domains:
            domain_to_insti[domain] = name
    return domain_to_insti

def get_email_to_history(emails):
    """Returns a mapping from emails to history data which may contain past institutions as well as domain"""
    
    history = dict()
    for email in emails.keys():
        history[email] = []
        if 'history' not in emails[email].content:
            continue
        notes = emails[email].content['history']
        for note in notes:
            # end date
            end = note['end'] if ('end' in note and isinstance(note['end'], int)) else -1
            # start date
            start = note['start'] if ('start' in note and isinstance(note['start'], int)) else -1
            # institution name
            insti = note['institution']
            period = [start, end, "", insti['name']]
            # add missing domain if possible, avoid email services such as gmail.com, yahoo.com, etc.
            if 'domain' in insti and '.' in insti['domain'] and len(insti['domain']) >= 3 and insti['domain'] not in email_services:
                period[2] = insti['domain']
            history[email].append(period)
    return history

def get_domain_to_all_possible_instis(email_to_history, wu_domain):
    """Returns a mapping from domain to all variations of an institution name"""
    
    domain_to_insti = dict()
    for email in email_to_history.keys():
        if len(email_to_history[email]) == 0:
            continue
        
        histories = email_to_history[email]
        
        for history in histories:
            domain, institution = history[2], history[3]
            if domain == "":
                continue
                
            for domain1 in wu_domain:
                if domain1 in domain:
                    domain = domain1
                    break
            
            history[2] = domain
            
            if domain in domain_to_insti:
                domain_to_insti[domain].append(institution)
            else:
                domain_to_insti[domain] = [institution]
        
    return domain_to_insti

def filter_institution_with_high_frequency_only(domain_to_insti_2):
    """Return a one on one mapping from domain to institution name"""
    def highest_frequency(institutions):
        count = dict()
        for institution in institutions:
            if institution in count:
                count[institution] += 1
            else:
                count[institution] = 1

        return max(count.items(), key=lambda k: k[1])[0]

    domain_to_insti = dict()
    for key in domain_to_insti_2.keys():
        domain_to_insti[key] = highest_frequency(domain_to_insti_2[key])
    return domain_to_insti

if __name__ == "__main__":

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
    
    # take advantange of world university domain dataset
    wu_json = pd.read_json("world_universities_and_domains.json")
    wu_domain = get_domain_to_insti_from_world_university(wu_json)
    
    emails = None
    with open("emails.p", 'rb') as fp:
        emails = pickle.load(fp)
   
    email_to_history = get_email_to_history(emails)

    domain_to_instis = get_domain_to_all_possible_instis(email_to_history, wu_domain)

    domain_to_insti = filter_institution_with_high_frequency_only(domain_to_instis)
    
    # clean email_to_history again with domain_to_insti just acquired
    # this dataset may be used to match institution name for author that cannot be inferred from their email domain.
    for email in email_to_history.keys():
        for history in email_to_history[email]:
            if history[2] == "":
                continue
            for domain in domain_to_insti.keys():
                if domain in history[2]:
                    history[2] = domain
                    history[3] = domain_to_insti[domain]
                    break
    
    # add the rest of world domains to domain_to_insti
    for key in wu_domain.keys():
        if key not in domain_to_insti:
            domain_to_insti[key] = wu_domain[key]
                    
    with open("domain_to_insti.p", 'wb') as fp:
        pickle.dump(domain_to_insti, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open("email_to_history.p", 'wb') as fp:
        pickle.dump(email_to_history, fp, protocol=pickle.HIGHEST_PROTOCOL)
