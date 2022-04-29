import re

from frozendict import frozendict

from serializer_lib.factory.parsers.parser import Parser
from serializer_lib.factory.parsers.json.constans import *


class ParserJson(Parser):

    def dump(self, obj, file):  # obj to file
        result = self.dumps(obj)
        file.write(result)

    def dumps(self, obj):  # obj to string
        ans = ""
        ans_list = []
        flag = False
        if type(obj) == frozendict or type(obj) == dict:
            for key, value in obj.items():
                if key == VALUE_FIELD or key == TYPE_FIELD:
                    ans_list.append("" + self.dumps(key) + ": " + self.dumps(value) + "")
                    flag = True
                else:
                    ans_list.append("[" + self.dumps(key) + ", " + self.dumps(value) + "]")
                    flag = False
            ans += ", ".join(ans_list)
            if flag:
                ans = "{" + ans + "}"
            else:
                ans = "[" + ans + "]"
            return f"{ans}"
        elif type(obj) == tuple:
            serialized = []
            for i in obj:
                serialized.append(f"{self.dumps(i)}")
            ans = ", ".join(serialized)
            return f"[{ans}]"
        else:
            return f"\"{str(obj)}\""


    def load(self, file):  # file to obj

        pass

    def loads(self, string):  # string to obj
        if string == '{}':
            return frozendict()
        elif string[0] == '{':
            ans = dict()
            string = string[1:len(string) - 1]
            if re.match(VALUE_REGEX1, string):
                temp = ""
                flag = False
                save_i = 0
                ans_list = []
                balance = 0
                balance2 = 0
                for i in range(8, len(string)):
                    if string[i] == '[' and not flag:
                        balance2 += 1
                    elif string[i] == ']' and not flag:
                        balance2 -= 1
                    elif string[i] == '{' and not flag:
                        balance += 1
                    elif string[i] == '}' and not flag:
                        balance -= 1
                    elif string[i] == '\"':
                        flag = not flag
                    elif string[i] == ',' and not flag and balance == 0 and balance2 != 0:
                        ans_list.append(self.loads(temp))
                        temp = ""
                        continue
                    elif string[i] == ' ' and not flag and balance == 0:
                        continue
                    elif string[i] == "," and not flag and balance2 == 0:
                        ans_list.append(self.loads(temp))
                        save_i = i
                        temp = ""
                        break
                    temp += string[i]

                ans[VALUE_FIELD] = {}
                for i in range(0, len(ans_list), 2):
                    ans[VALUE_FIELD][ans_list[i]] = ans_list[i+1]

                temp = ""
                for i in range(save_i + 11, len(string)):
                    if string[i] == '\"':
                        ans[TYPE_FIELD] = temp
                        temp = ""
                        break
                    else:
                        temp += string[i]
            elif re.match(VALUE_REGEX2, string):
                temp = ""
                flag = False
                save_i = 0
                ans_list = []
                balance = 0
                for i in range(10, len(string)):
                    if string[i] == '{' and not flag:
                        balance += 1
                    elif string[i] == '}' and not flag:
                        balance -= 1
                    if string[i] == '\"':
                        flag = not flag
                    elif string[i] == ',' and not flag and balance == 0:
                        ans_list.append(self.loads(temp))
                        temp = ""
                        continue
                    elif string[i] == ' ' and not flag and balance == 0:
                        continue
                    elif string[i] == "]" and not flag and balance == 0:
                        ans_list.append(self.loads(temp))
                        save_i = i
                        temp = ""
                        break
                    temp += string[i]

                ans[VALUE_FIELD] = ans_list

                for i in range(save_i + 12, len(string)):
                    if string[i] == '\"':
                        ans[TYPE_FIELD] = temp
                        temp = ""
                        break
                    else:
                        temp += string[i]
            else:
                temp = ""
                flag = False
                i = 10
                while i < len(string):
                    if string[i] == '\"' and not flag:
                        ans[VALUE_FIELD] = temp
                        temp = ""
                        flag = True
                        i += 11
                    elif string[i] == '\"' and flag:
                        ans[TYPE_FIELD] = temp
                        temp = ""
                        break
                    else:
                        temp += string[i]
                    i+=1
            return frozendict(ans)
