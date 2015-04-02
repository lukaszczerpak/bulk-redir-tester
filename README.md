# bulk-redir-tester

Very simple tool to test large volume of http redirects.
 
# How it works

`redir-tester.py` takes two arguments:

- <redirs_spec> - filename with list of redirections to be tested
- <hostname> - hostname against which all tests will be performed

Note: The tools doesn't connect hostname specified in source URL, but hostname provided as command argument. Source URL is used only to set HOST header appropriately.
 
## Redirections spec file format
 
It's plain CSV. Fields are delimited by single whitespace ' ', example:

```
301 http://localhost:8989/test1 http://localhost/target1
302 http://localhost:8989/test2 /target2
302 http://localhost:8989/ /about/
```

# Mock server

`sample-server.py` is a simple mock server to return redirects specified in JSON file:

```
sample-server.py sample-redirs.json
```

The above command will run local server on port 8989. Once up and running you can run test suite as follows:

```
redir-tester.py test1.csv
```


