# PyParser

PyParser is a vulnerability parser that looks for CVE's from different sources. It employs the Shodan API, has the ability to retrieve and process data from [CVE Mitre](https://cve.mitre.org/) and comes with functionality to install and use Offensive Security's ExploitDB [Searchsploit](https://github.com/offensive-security/exploit-database/blob/master/searchsploit) utility.

## Usage

Start the program from the command line with `python cveparser.py`. Once the program has been started it will prompt for your Shodan.io API key. Once provided it will prompt to install Searchsploit, which is optional. After these operations a menu will be displayed the options for which are as follows.

```
1. Query Shodan				4. Logging	
2. Query CVE Mitre			5. Quit
3. Invoke Searchsploit				
```
Select a number to select a data source to use when searching for a particular vulnerability. The 'logging' option will save results of your search queries in the current working directory as an application log from PyParser.

## Dependencies
PyParser depends on the following Python 2.7 libraries.
```
blessings
shodan
pycurl
```
Should you find you do not have any of these libraries installed please use Python's built in package manager to resolve it like so `pip install blessings` etc.

### Note

This is a BETA release, as such there might be some bugs. If you happen to encounter a bug please feel free to [open a ticket](https://github.com/NullArray/PyParser/issues) or [submit a pull request](https://github.com/NullArray/PyParser/pulls)
