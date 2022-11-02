Note: Output of array is disabled by default because the log limit is reached before the stack limit. To properly log the array uncomment line 55 in [golf.rb](./golf.rb)

# Running Script
## Install py deps
```
pip install -U --force-reinstall git+https://github.com/algorand-devrel/beaker@boxen
pip install -U --force-reinstall git+https://github.com/algorand/pyteal@avm8
pip install -U --force-reinstall git+https://github.com/algorand/py-algorand-sdk@feature/box-storage
```

## Run python script
```
python golf.py
```

# Modifying TEAL
# Install ruby deps
```
bundle install
```

# Recompile TEALrb
```
bundle exec ruby golf.py
```