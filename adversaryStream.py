from stairwaytoheaven import StairwayToHeaven as sketch
import bisect
from math import inf

class Adversary:
    def __init__(self, sketchsize, inveps):
        self.sketchsize = sketchsize
        self.inveps = inveps

    def get_between(self, left, right, count):
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

    def refineIntervals(self, pi, rho, l_pi, r_pi, l_rho, r_rho):
        sketch_pi = sketch(self.sketchsize, (inf,), (-inf,))
        sketch_rho = sketch(self.sketchsize, (inf,), (-inf,))
        for x in pi:
            sketch_pi.update(x)
        for x in rho:
            sketch_pi.update(x)
        mem_pi = sorted(sketch_pi.get_memory())
        mem_pi = [l_pi] + [x for x in mem_pi if x>l_pi and x<r_pi] + [r_pi]
        mem_rho = sorted(sketch_rho.get_memory())
        mem_rho = [l_rho] + [x for x in mem_rho if x>l_rho and x<r_rho] + [r_rho]

        I = 0
        maxdiff = -1
        for i in range(0, len(mem_rho)-1):
            dif = bisect.bisect_left(sorted(rho), mem_rho[i+1]) - bisect.bisect_left(sorted(pi), mem_pi[i])
            if dif > maxdiff:
                I = i
                dif = maxdiff

        alpha_pi = mem_pi[I]
        beta_pi = sorted(pi)[bisect.bisect_left(sorted(pi),mem_pi[I]) + 1]

        j = bisect.bisect_left(sorted(rho), mem_rho[I+1])
        if j==0:
            alpha_rho = (-inf,)
        else:
            alpha_rho = sorted(rho)[j-1]
        beta_rho = mem_rho[I+1]
        return (alpha_pi, beta_pi, alpha_rho, beta_rho)

    def advStrategy(self, k, pi, rho, l_pi, r_pi, l_rho, r_rho):
        if k==1:
            pi2 = pi + self.get_between(l_pi, r_pi, 2*self.inveps)
            rho2 = rho + self.get_between(l_rho, r_rho, 2*self.inveps)
            return (pi2, rho2)
        else:
            (pi1, rho1) = self.advStrategy(k-1, pi, rho, l_pi, r_pi, l_rho, r_rho)
            (alpha_pi, beta_pi, alpha_rho, beta_rho) = self.refineIntervals(pi1, rho1, l_pi, r_pi, l_rho, r_rho)
            return self.advStrategy(k-1, pi1, rho1, alpha_pi, beta_pi, alpha_rho, beta_rho)


    def generateStream(self, k:int):
        # generate streams of tuples (compared using lexico order)
        pi, rho = self.advStrategy(k, (), (), (-inf,), (inf,), (-inf,), (inf,) )
        # convert to streams of numbers
        
        sketch_pi = sketch(self.sketchsize, (inf,), (-inf,))
        sketch_rho = sketch(self.sketchsize, (inf,), (-inf,))
        for x in pi:
            sketch_pi.update(x)
        for x in rho:
            sketch_pi.update(x)
        
        if sketch_pi.get_error()>sketch_rho.get_error():
            stream = pi
        else:
            stream = rho

        sorted_list = sorted(list(set(stream)))

        return_stream = []
        for x in stream:
            return_stream += [bisect.bisect_left(sorted_list, x)]
        return return_stream
