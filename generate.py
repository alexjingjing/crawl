from app.model import Session
from app.model.deparr import DepArr

cities = ['北京', '上海', '广州', '深圳', '成都', '重庆', '厦门', '昆明', '杭州', '西安', '武汉', '长沙', '南京', '大连', '郑州', '青岛', '天津', '三亚',
          '海口', '乌鲁木齐']

if __name__ == '__main__':
    session = Session()
    for i in range(len(cities)):
        for j in range(len(cities)):
            if j + 1 == len(cities):
                break
            print('1{}, 2{}'.format(cities[0], cities[j + 1]))
            session.add(DepArr(cities[0], cities[j + 1]))
            session.commit()
        cities.append(cities[0])
        cities.remove(cities[0])
