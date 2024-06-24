option = {
    graphic: {
      elements: [
        
        {
          type:"image",
          x:500,
          y:100,
          scaleX:5,
          scaleY:5,
          style: {
            image:"https://dashboard.daten.city/assets/climate_black_on_transparent-DttMZn_n.svg",
            x:0,
            y:0,
            width:100,
            height:100,
          },
        },
        {
          type:"image",
          style: {
            image:"https://dashboard.daten.city/assets/logo-CqImCqPj.png",
            x:300,
            y:0,
            width:100,
            height:100,
            color:"#ff0",
          },
        },
        {
          type:"image",
          style: {
            image:"http://localhost:5173/images/tiles/lastenrad.jpg",
            x:100,
            y:100,
            width:100,
            height:100,
          },
        },
        {
          type: 'group',
          x: 500,
          y: 100,
          children: [
            {
              type:"rect",
              x:0,
              shape: {
                x: 0,
                y: 0,
                width: 20,
                height: 20
              },
              style: {
                fill: 'red'
              },
            },
            {
              type:"rect",
              x:40,
              shape: {
                x: 0,
                y: -40,
                width: 20,
                height: 60
              },
              style: {
                fill: 'blue'
              },
            },
            ],
        }
      ]
    }
  };