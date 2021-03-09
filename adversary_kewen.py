from stairwaytoheaven import StairwayToHeaven as sketch
import bisect
from math import inf

class AdversaryKewen:
    def __init__(self, sketchsize):
        self.sketchsize = sketchsize

    def get_between(self, left, right, count=1):
        strict = False
        if (len(left) < len(right)):
            for i in range(len(left)):
                if left[i] < right[i]:
                    strict = True
        else:
            strict = True
        if not strict:
            left += (right[len(left)] - 1,)
        return_list = ()
        for i in range(count):
            return_list += ( left +  (i,), )
        return return_list


    def generateStream(self, n:int):
        sk = sketch(self.sketchsize, (inf,), (-inf,))

        stream = ()
        for i in range(n):
            x1,x2 = sk.max_error_range()
            print(f'x1,x2={(x1,x2)}')
            x = self.get_between(x1, x2)
            print(f'x={(x[0])}')
            print('x={(x[0])}')
            stream += x
            sk.update(x[0])

        sorted_list = sorted(list(set(stream)))

        return_stream = []
        for x in stream:
            return_stream += [bisect.bisect_left(sorted_list, x)]
        return tuple(return_stream)
