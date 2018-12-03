### 身份组成方式

[中华人民共和国国家标准](https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%9B%BD%E5%AE%B6%E6%A0%87%E5%87%86)[GB 11643-1999《公民身份号码》](https://zh.wikisource.org/wiki/GB_11643-1999_%E5%85%AC%E6%B0%91%E8%BA%AB%E4%BB%BD%E5%8F%B7%E7%A0%81)中规定：公民身份号码是特征组合码，由十七位数字本体码和一位校验码组成。

18位数字组合的方式是：

| 1 1 0 1 0	2 | Y Y	Y Y	M M D D | 8 8 | 8 | X |
| :---------: | :---------------: | :----: | :--: | :----: |
|    区域码(6位)    |  出生日期码(8位)     | 顺序码(2位) | 性别码(1位) | 校验码(1位) |


- **区域码** 指的是公民常住户口所在县（市、镇、区）的[行政区划代码](https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BB%A3%E7%A0%81)，如110102是[北京市](https://zh.wikipedia.org/wiki/%E5%8C%97%E4%BA%AC%E5%B8%82)[西城区](https://zh.wikipedia.org/wiki/%E8%A5%BF%E5%9F%8E%E5%8C%BA)。但港澳台地区居民的身份号码只精确到省级。
- **出生日期码** 表示公民出生的公历年（4位）、月（2位）、日（2位）。
- **顺序码 ** 表示在同一区域码所标识的区域范围内，对同年、同月、同日出生的人编定的顺序号。
- **性别码** 奇数表示男性，偶数表示女性。
- 最后一位是**校验码**，这里采用的是**ISO 7064:1983,MOD 11-2**校验码系统。校验码为一位数，但如果最后采用校验码系统计算的校验码是“10”，碍于身份证号码为18位的规定，则以“X”代替校验码“10”。

### 校验码计算方法

-  **1.** 将身份证号码从右至左标记为$$a_1 , a_2 , \cdots , a_{18}$$，$$a_1$$即为校验码；
-  **2. ** 计算权重系数 $$ W_i=2^{i-1}\  \bmod \ {11}  $$

所以:


|**i**|18|17|16|15|14|13|12|11|10|9|8|7|6|5|4|3|2|1|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:| :-:| :-:|
| **W<sub>i</sub>** |7|9|10|5|8|4|2|1|6|3|7|9|10|5|8|4|2|1|

- **3.**   计算$$ S = \sum_{i=2}^{18} a_i \cdot W_i $$
- **4.**   $$ a_1=(12-( S \ \bmod 11)) \bmod 11 $$

使用[Python](https://zh.wikipedia.org/wiki/Python)获取身份证校验码：
```Python
def get_check_digit(id_number):
    """通过身份证号获取校验码"""
    check_sum = 0
    for i in range(0, 17):
        check_sum += ((1 << (17 - i)) % 11) * int(id_number[i])
    check_digit = (12 - (check_sum % 11)) % 11
    return check_digit if check_digit < 10 else 'X'
```



### 随机生成身份证

由上面的组合方式我们可以得出以下代码:

 ```python
@classmethod
def generate_id(cls, sex=0):
    """
     随机生成身份证号，sex = 0表示女性，sex = 1表示男性
    """

    # 随机生成一个区域码(6位数)
    area_info = random.randint(0, len(addr))
    id_number = str(addr[area_info][0])

    # 限定出生日期范围(8位数)
    start, end = "1960-01-01", "2000-12-30"

    days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
    birth_days = datetime.datetime.strftime(
        datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d"
    )

    id_number += str(birth_days)
    # 顺序码(2位数)
    id_number += str(random.randint(9, 99))
    # 性别码(1位数)
    id_number += str(random.randrange(sex, 10, step=2))
    # 校验码(1位数)
    return id_number + str(cls(id_number).get_check_digit())
 ```



### 工具类主要功能

```python
if __name__ == '__main__':
    random_sex = random.randint(0, 1)  # 随机生成男(1)或女(0)
    print IdNumberUtil.generate_id(random_sex)  # 随机生成身份证号
    print IdNumberUtil('410326199507103197').area_id  # 地址编码:410326
    print IdNumberUtil('410326199507103197').get_area_name()  # 地址:汝阳县
    print IdNumberUtil('410326199507103197').get_birthday()  # 生日:1995-7-10
    print IdNumberUtil('410326199507103197').get_age()  # 年龄:23(岁)
    print IdNumberUtil('410326199507103197').get_sex()  # 性别:1(男)
    print IdNumberUtil('410326199507103197').get_check_digit()  # 校验码:7
    print IdNumberUtil.verify_id('410326199507103198')  # 检验身份证是否正确:False
```

[代码地址]: https://github.com/jayknoxqu/id-number-util
