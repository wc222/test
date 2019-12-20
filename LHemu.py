import pyhash
import random

class LHe:
    def __init__(self):
        self.h1 = pyhash.fnv1_64()
        self.h2 = pyhash.metro_64()
        self.empty_bucket = [(0,0)]*4
        self.TL = []
        self.BL = []
        self.TMP = []
        self.N = 0

        print('Welcome to Level Hashing emulator!')
        t = input('Please configure Top Level size N = 2^')
        try:
            t = int(t)
            print('Set N =',2**t, ', initialize successfully')
            self.N = 2**t
            self.TL = [self.empty_bucket.copy() for i in range(self.N)]
            self.BL = [self.empty_bucket.copy() for i in range(self.N//2)]
        except ValueError:
            print('Error : the input is not a int')
            return
        
        self.cui()

    def access_bucket(self, is_top, pos, key):
        l = self.TL if is_top else self.BL
        b = l[pos]
        ret = {'empty':0, 'hit':0}
        for i in range(4):
            if b[i][0] == 0:
               ret['empty'] += 1
            elif b[i][1] == key:
                ret['hit'] = 1
        return ret

    def modify_bucket(self, is_top, pos, key, is_insert):
        l = self.TL if is_top else self.BL
        b = l[pos]
        if is_insert:
            for i in range(4):
                if b[i][0] == 0:
                    b[i] = (1, key)
                    break
            else:
                raise Exception
        else:
            for i in range(4):
                if b[i][0] and b[i][1] == key:
                    b[i] = (0,0)
                    break
            else:
                raise Exception
        return 

    def find_alt(self, is_top, pos):
        l = self.TL if is_top else self.BL
        b = l[pos]
        N = self.N if is_top else self.N//2
        for (f,k) in b:
            if f:
                pk1 = self.h1(k)%N
                pk2 = self.h2(k)%N
                alt = pk1 if pk1 != pos else pk2
                if self.access_bucket(is_top, alt, k)['empty']:
                    return (alt, k)
            else:
                raise Exception
        return None


    def insert(self, key, directly=0):
        pos1 = self.h1(key)%self.N
        pos2 = self.h2(key)%self.N
        if not directly:
            print('First position is {:d}; Second position is {:d}'.format(pos1, pos2))
            self.print_data()
            input()
        else:
            print('First position is {:d}; Second position is {:d}'.format(pos1, pos2))
            self.print_data()
        
        is_TL = True
        idx1 = pos1
        idx2 = pos2
        for i in range(2):
            ret1 = self.access_bucket(is_TL, idx1, key)
            ret2 = self.access_bucket(is_TL, idx2, key)
            #已经存在
            if ret1['hit'] or ret2['hit']:
                print('Insertion failed because the key exists at', 'TL' if is_TL else 'BL', idx1 if ret1['hit'] else idx2 )
                break
            #有空位
            elif ret1['empty'] or ret2['empty']:
                if ret1['empty'] > ret2['empty']:
                    self.modify_bucket(is_TL, idx1, key, True)
                    if not directly:
                        print("Insert in {} {} because less-loaded".format('TL' if is_TL else 'BL', idx1))
                        input()
                    else:
                        print("Insert in {} {} because less-loaded".format('TL' if is_TL else 'BL', idx1))
                elif ret1['empty'] < ret2['empty']:
                    self.modify_bucket(is_TL, idx2, key, True)
                    if not directly:
                        print("Insert in {} {} because less-loaded".format('TL' if is_TL else 'BL', idx2))
                        input()
                    else:
                        print("Insert in {} {} because less-loaded".format('TL' if is_TL else 'BL', idx2))
                else:
                    if random.randint(0,9)%2 == 0:
                        self.modify_bucket(is_TL, idx1, key, True)
                        if not directly:
                            print("Insert in {} {} because randomly broke tie".format('TL' if is_TL else 'BL', idx1))
                            input()
                        else:
                            print("Insert in {} {} because randomly broke tie".format('TL' if is_TL else 'BL', idx1))
                    else:
                        self.modify_bucket(is_TL, idx2, key, True)
                        if not directly:
                            print("Insert in {} {} because randomly broke tie".format('TL' if is_TL else 'BL', idx2))
                            input()
                        else:
                            print("Insert in {} {} because randomly broke tie".format('TL' if is_TL else 'BL', idx2))
                break
            #翻转
            else:
                is_TL = False
                idx1 //= 2
                idx2 //= 2
                if i == 0:
                    if not directly:
                        print("Two TL buckets have been full, try to insert in BL")
                        input()
                    else:
                        print("Two TL buckets have been full, try to insert in BL")
        #四个位置插入失败, 考虑在转移一个项
        else:
            if not directly:
                print("Two BL buckets have been full, try to move an item in TL")
                input()
            else:
                print("Two BL buckets have been full, try to move an item in TL")
            is_TL = True
            idx1 = pos1
            idx2 = pos2
            for i in range(2):
                ret1 = self.find_alt(is_TL, idx1)
                ret2 = self.find_alt(is_TL, idx2)
                if ret1 != None or ret2 != None:
                    ((alt_p, alt_k), pos) = (ret1, idx1) if ret1 != None else (ret2, idx2)
                    if not directly:
                        print("Found an viable move of",alt_k,'from',pos,'to',alt_p)
                        input()
                    else:
                        print("Found an viable move of",alt_k,'from',pos,'to',alt_p)
                    self.modify_bucket(is_TL, alt_p, alt_k, True)
                    if not directly:
                        print("First insert",alt_k,'at',alt_p)
                        input()
                        self.print_data()
                        input()
                    else:
                        print("First insert",alt_k,'at',alt_p)
                    self.modify_bucket(is_TL, pos, alt_k, False)
                    if not directly:
                        print("Second delete",alt_k,'from',pos)
                        input()
                        self.print_data()
                        input()
                    else:
                        print("Second delete",alt_k,'from',pos)
                    self.modify_bucket(is_TL, pos, key, True)
                    if not directly:
                        print("Finally insert",key,'at',pos)
                        input()
                        self.print_data()
                        input()
                    else:
                        print("Finally insert",key,'at',pos)
                    break
                else:
                    is_TL = False
                    idx1 //= 2
                    idx2 //= 2
                    if i == 0:
                        if not directly:    
                            print("No item in two TL buckets could be moved, try the BL")
                            input()
                        else:
                            print("No item in two TL buckets could be moved, try the BL")
            #四个位置都转移失败,重置后插入
            else:
                if not directly:
                    print("No item in two BL buckets could be moved, need to risize")
                    input()
                else:
                    print("No item in two BL buckets could be moved, need to risize")
                self.resize()
                print("Resize successfully")
                self.insert(key,directly)
                return

        print('\nAfter insertion')
        self.print_data()
        return 


    def search(self, key, directly=0):
        pos1 = self.h1(key)%self.N
        pos2 = self.h2(key)%self.N
        if not directly:
            self.print_data()
            print('First position is {:d}; Second position is {:d}'.format(pos1, pos2))
            input()
        else:
            print('First position is {:d}; Second position is {:d}'.format(pos1, pos2))
        
        is_TL = True
        idx1 = pos1
        idx2 = pos2
        for i in range(2):
            ret1 = self.access_bucket(is_TL, idx1, key)
            ret2 = self.access_bucket(is_TL, idx2, key)
            #已经存在
            if ret1['hit'] or ret2['hit']:
                print('Find the key at', 'TL' if is_TL else 'BL', idx1 if ret1['hit'] else idx2 )
                break
            else:
                is_TL = False
                idx1 //= 2
                idx2 //= 2
                if i == 0:
                    if not directly:
                        print("Not found the key in two TL buckets, try the BL buckets")
                        input()
                    else:
                        print("Not found the key in two TL buckets, try the BL buckets")
        else:
            print("Not found the key in two BL buckets")
            print("So there is not key as",key, "in Level Hashing")

    def delete(self, key, directly=0):
        pos1 = self.h1(key)%self.N
        pos2 = self.h2(key)%self.N
        if not directly:
            self.print_data()
            print('First position is {:d}; Second position is {:d}'.format(pos1, pos2))
            input()
        else:
            print('First position is {:d}; Second position is {:d}'.format(pos1, pos2))
        
        is_TL = True
        idx1 = pos1
        idx2 = pos2
        for i in range(2):
            ret1 = self.access_bucket(is_TL, idx1, key)
            ret2 = self.access_bucket(is_TL, idx2, key)
            #已经存在
            if ret1['hit'] or ret2['hit']:
                print('Find the key to delete at', 'TL' if is_TL else 'BL', idx1 if ret1['hit'] else idx2)
                self.modify_bucket(is_TL, idx1 if ret1['hit'] else idx2, key, False)
                break
            else:
                is_TL = False
                idx1 //= 2
                idx2 //= 2
                if i == 0:
                    if not directly:
                        print("Not found the key in two TL buckets, try the BL buckets")
                        input()
                    else:
                        print("Not found the key in two TL buckets, try the BL buckets")
        else:
            print("Not found the key in two BL buckets")
            print("So there is not key as",key, "in Level Hashing")

        print("After deletion")
        self.print_data()

    def resize(self):
        self.TMP = self.BL
        self.BL = self.TL
        self.TL = [self.empty_bucket.copy() for i in range(self.N * 2)]
        for i in range(self.N//2):
            for f,k in self.TMP[i]:
                if f:
                    self.insert(k, 1)
        self.TMP = []
        self.N *= 2

    def print_data(self):
        # print(self.TL)
        # print(self.BL)
        print()
        self.__print_helper(True)
        print()
        self.__print_helper(False)
        print()
    
    def __print_helper(self, is_top):
        incident, L, N = (' '*0, self.TL, self.N) if is_top else (' '*4, self.BL, self.N//2)
        #top
        print(incident,end='')
        for i in range(N):
            print('+',end='')
            if i < 10:
                print("---{:d}--+".format(i),end='')
            else:
                print("--{:d}--+".format(i),end='')
            if not is_top:
                print(' '*8,end='')
        print()
        #data
        for i in range(4):
            print(incident,end='')
            for j in range(N):
                print('|',end='')
                if L[j][i][0]:
                    print(' {} |'.format(L[j][i][1]),end='')
                else:
                    print('      |',end='')
                if not is_top:
                    print(' '*8,end='')
            print()

        #bottom
        print(incident,end='')
        for i in range(N):
            print('+',end='')
            print('------+',end='')
            if not is_top:
                print(' '*8,end='')
        print()

    def cui(self):
        err_cmd_promt = "Unknown cmd. Type 'help' for help"
        last_one = ''
        while(1):
            print("\n************************************")
            cmd = input('> ')
            if cmd.strip() == '':
                cmd = last_one
            else:
                last_one = cmd
            print("\n")
            cl = cmd.split()
            # cmd length is 1: help/print/q
            if len(cl) == 1:
                if cl[0] == 'help' or cl[0] == 'h':
                    print("Usage:")
                    print("  print : to print the data structure")
                    print("  insert 'key' [d] : to insert the key directly or step by step")
                    print("  delete 'key' [d] : to delete the key directly or step by step")
                    print("  search 'key' [d] : to search the key directly or step by step")
                    print("  q : quit")
                elif cl[0] == 'print' or cl[0] == 'p':
                    self.print_data()
                elif cl[0] == 'q':
                    break
                else:
                    print(err_cmd_promt)
            # cmd length is 2: insert/delete/search
            elif len(cl) <= 3:
                key = self.get_key(cl[1])
                if key == None:
                    continue
                if len(cl) <= 2 or cl[2].strip() == '':
                    d = 0 
                else:
                    d = 1
                
                if cl[0] == 'insert' or cl[0] == 'i':
                    self.insert(key, d)
                elif cl[0] == 'delete' or cl[0] == 'd':
                    self.delete(key, d)
                elif cl[0] == 'search' or cl[0] == 's':
                    self.search(key, d)
                else:
                    print(err_cmd_promt)
            else:
                print(err_cmd_promt)

    def get_key(self, s):
        if s == 'r':
            key = self.r()
        else:
            try:
                key = '{:04d}'.format(int(s)%int(1e5))
            except:
                print('error : key is not a number ->', s)
                key = None
        return key
            

    def r(self):
        t = str(random.randint(1e3,1e4-1))
        print('gen a random int : ',t)
        print()
        return t


if __name__ == "__main__":
    a = LHe()
