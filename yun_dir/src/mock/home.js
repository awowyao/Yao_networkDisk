import Mock from 'mockjs'

export default {
  getHomeData: () => {
    return {
      code: 20000,
      data: {
        videoData: [
          {
            name: 'SpromgBoot',
            value: Mock.Random.float(1000, 20000, 0, 2)
          },
          {
            name: 'Vue',
            value: Mock.Random.float(1000, 20000, 0, 2)
          },
          {
            name: '小程序',
            value: Mock.Random.float(1000, 20000, 0, 2)
          }
        ]
      }
    }
  }
}
