import json


class CircuitNetwork:
    def __init__(self, channels=[]):
        self.channels = channels
    def __call__(self, channel=None):
        "Shorthand for new()"
        return self.add(channel)
    def __add__(self, other): # Combining networks
        channels = self.channels.copy()
        channels.extend(other.channels)

        x = self.__class__(channels)
        x.cleanup()
        return x


    def add(self, channel=None):
        if hash(channel) == hash(None):
            channel = self.Channel()

        self.channels.append(channel)
        return channel
        
    def cleanup(self):
        # Remove duplicate channels

        i = 0
        while i < len(self.channels):

            j = i + 1
            while j < len(self.channels):

                # Channel objects handle "==" differently, so use hash()
                if hash(self.channels[i]) == hash(self.channels[j]):
                    # If identical, remove the second one
                    self.channels.pop(j)

                else:
                    # Move on to the next comparison
                    j += 1
            
            # Cleanup the current channel
            #self.channels[i].cleanup() TODO

            i += 1
        

        # Anything more???

    def export(self, jsonFormattable=False, doCleanup=True):
        if doCleanup:
            self.cleanup()

        if jsonFormattable:
            return [i.export(True, doCleanup=doCleanup) for i in self.channels]
        
        else:
            return self.channels


    class Channel: # https://docs.python.org/3/reference/datamodel.html#special-method-names
        "IMPORTANT: use hash(x) == hash(y) NOT x == y when comparing Channels in a boolean context (e.g. if statements)"

        def __init__(self):
            self.data = []
        def __call__(self, x):
            "Shorthand for add()"
            return self.add(x)
            
        def __hash__(self):
            # Lists are not hashable, so convert the data to a tuple of tuples
            return hash(tuple([tuple(i) for i in self.data]))
        
        def add(self, x):
            self.data.append(x)
            return x
        
        def cleanup(self):
            raise NotImplementedError

            # Add duplicate combinators

            i = 0
            while i < len(self.data):

                j = i + 1
                while j < len(self.data):
                    if self.data[i] == self.data[j]:
                        print(i, j)

                        ## If identical, add them, and remove the second one
                        #second = self.data.pop(j)

                    else:
                        # Move on to the next comparison
                        j += 1

                i += 1
            

            # Anything more???
        
        def export(self, jsonFormattable=False, doCleanup=False):
            if doCleanup:
                self.cleanup()
            
            if jsonFormattable:
                data = []
                for i in self.data:
                    if isinstance(i, self.__class__):
                        data.append(i.export(True))
                    
                    else:
                        data.append(i)

                return data
            
            else:
                return self.data


        # Arithmetic
        def __add__(self, other):
            return [self, "+", other]
        def __sub__(self, other):
            return [self, "-", other]
        def __mul__(self, other):
            return [self, "*", other]
        #def __matmul__(self, other): # Matrix multiplication
        #    return
        #def __div__(self, other): # No! Use __truediv__()
        #    return
        def __truediv__(self, other): # Shorthand for __floordiv__()
            return self.__floordiv__(other)
        def __floordiv__(self, other):
            return [self, "/", other]
        def __mod__(self, other):
            return [self, "%", other]
        #def __divmod__(self, other): # I will make use of divmod() later, but there is no combinator for it...
        #    return
        def __pow__(self, other):
            return [self, "^", other]
        def __lshift__(self, other):
            return [self, "<<", other]
        def __rshift__(self, other):
            return [self, ">>", other]
        def __and__(self, other):
            return [self, "AND", other]
        def __or__(self, other):
            return [self, "OR", other]
        def __xor__(self, other):
            return [self, "XOR", other]


        # Decider
        def __lt__(self, other):
            return [self, "<", other]
        def __le__(self, other):
            return [self, "≤", other]
        def __eq__(self, other):
            return [self, "=", other]
        def __ne__(self, other):
            return [self, "≠", other]
        def __gt__(self, other):
            return [self, ">", other]
        def __ge__(self, other):
            return [self, "≥", other]



manager = CircuitNetwork()


#time = manager()
#time(time+1)

#mod = manager()
#mod(time%120)

#out = manager()
#out(mod<60)


# 5 copies
x = manager()
x("asdf")
manager(x)("qwerty")

print(manager.channels)


raw = manager.channels
clean = manager.export(True)

print(raw)
print()
print(clean)
#print()
#print(json.dumps(raw, indent=4))
#print()
#print(json.dumps(clean, indent=4))
