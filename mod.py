import re
def main(time:str, domains:list[str], mode):
    '''gets list of domains and returns sorted by domain in alphabetical order'''    
    already = l = []
    entries = f'# {time}'

    for i in domains:
        if t := re.findall(r'\w+\.\w+$', i):
            print(i)
            l.append([i.split(t[0])[0], t[-1]])
        else:pass
    l = sorted(l, key = lambda x: x[::-1])
    
    for i in l:
        domain = i[-1]
        if domain not in already:
            ae=[j if j[-1] == domain else None for j in l]
            ae=list(filter(None, ae))

            so_ = sorted(ae, key = lambda x: x[::-1])

            if mode=='hosts':
                entries += f'\n# {domain}\n' + '\n0.0.0.0'.join([''.join(j) for j in so_])+'\n'

            elif mode=='adblock':
                entries += \
                    f'\n# {domain}\n' \
                    +'\n'.join(['||{}^'.format(entry) for entry in [''.join(j) for j in so_]]) \
                    +'\n'
            else:
                assert False

            already.append(domain)
    return entries

if __name__=='__main__':
    # test it
    l=main(['csp.report.yandex.net', 'static.com.yandex', 'google.com', 'app.google'])
    print(l)