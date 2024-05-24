window.onload = function() {
    // 创建地图实例
    var map = new AMap.Map('map', {
        center: [103.988918,30.582179], // 初始地图中心点
        zoom: 17 // 初始地图缩放级别
    });

    distance = 1000
    school_site = 0
    track = ""

    // 像后端发送数据请求
    function sendAndDisplay(distance, school_site) {
        // 构建请求的 URL
        var url = '/api/getTrack';
        
        // 创建包含 distance 和 school_site 的对象作为请求的 payload
        var data = {
            distance: distance,
            school_site: school_site
        };
        
        // 发起 AJAX POST 请求获取坐标点数据
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // 获取到数据后进行处理
                    var trackData = JSON.parse(xhr.responseText);
        
                    // 从 JSON 数据中提取 track 字段的值
                    var trackValue = trackData.track;
                    track = trackValue;
        
                    // 去除字符串开头和结尾的方括号
                    trackValue = trackValue.replace(/^\[|\]$/g, '');
        
                    // 使用 replace() 方法去除双引号
                    trackValue = trackValue.replace(/"/g, '');
        
                    // 将数据字符串以逗号分割成数组
                    var trackArray = trackValue.split(',');   
                    
                    // 初始化一个空数组，用于存储提取到的经纬度信息
                    var coordinates = [];
                        
                    // 遍历整个数据数组，逐个提取经纬度信息
                    for (var i = 0; i < trackArray.length; i += 1) {
                        // 获取当前元素
                        var point = trackArray[i];
                        // 将每个元素以连字符分割成经度和纬度
                        var coords = point.split('-');
                        // 将经度和纬度作为数组添加到 coordinates 数组中
                        coordinates.push([parseFloat(coords[0]), parseFloat(coords[1])]);
                    }
                    
                    // 清除地图上的轨迹线
                    map.clearMap();
                    // 调用绘制轨迹的函数
                    displayTrack(coordinates);
                } else {
                    console.error('请求失败：' + xhr.status);
                }
            }
        };
        // 将对象转换为 JSON 字符串并发送
        xhr.send(JSON.stringify(data));

        // 处理数据并在地图上展示
        function displayTrack(coordinates) {
            // 创建轨迹线对象
            var polyline = new AMap.Polyline({
                path: coordinates, // 设置轨迹线坐标数组
                strokeColor: '#FF0000', // 轨迹线颜色
                strokeWeight: 3, // 轨迹线宽度
                strokeOpacity: 1 // 轨迹线透明度
            });
    
            // 添加起点和终点标记（函数内的全局变量）
            var startPoint = coordinates[0]; // 起点坐标
            var endPoint = coordinates[coordinates.length - 1]; // 终点坐标
            addMarker(startPoint, '起点', coordinates); // 定义起点标记的样式和图标
            addMarker(endPoint, '终点', coordinates); // 定义终点标记的样式和图标

            // 将轨迹线添加到地图中
            map.add(polyline);
    
            // 调整地图视角以展示整条轨迹
            map.setFitView();
                            
        }
    
        // 添加标记函数
        function addMarker(position, title, coordinates) {
            // 自定义起点和终点标记的图标
            var iconUrl = 'https://kod.can6.top/?explorer/share/file&hash=48eccVyv4xCIzdYSX2Vrohonx3kJHCHgQG3WUElqg_uMOnBThaddGhfZtVlcqts0xQ&name=/%E5%9C%B0%E5%9B%BE-%E5%9C%B0%E6%A0%87.png';
    
            // 创建图标标记对象
            var marker = new AMap.Marker({
                position: position, // 标记位置
                title: title, // 标记标题
                offset: new AMap.Pixel(-12.5, -30), // 调整图标的原点位置
                icon: new AMap.Icon({
                    size: new AMap.Size(25, 25),  // 图标尺寸
                    image: iconUrl, // 图标的 URL
                    imageSize: new AMap.Size(25, 25)  // 图标显示大小
                })
            });
    
            // 创建文本标签对象
            var label = new AMap.Text({
                text: title, // 文本内容
                position: position, // 文本位置，与标记位置一致
                offset: new AMap.Pixel(13, -30), // 设置标签的偏移量，使其显示在标记的正上方
                style: {
                    color: 'bule', // 文本颜色
                    fontSize: 5, // 文本字号
                    // fontWeight: 'bold' // 文本加粗
                }
            });
    
            // 将图标标记添加到地图中
            marker.setMap(map);
            // 将文本标签添加到地图中
            label.setMap(map);

            // 如果是起点标记，则开始移动标记
            // if (position === coordinates[0]) {
            //     moveMarker(marker, coordinates, 5000); // 5000 毫秒为移动时长
            // }    
        }

        // 移动标记的函数
        function moveMarker(marker, path, duration) {
            var index = 0; // 当前路径点索引
            var startTime = new Date().getTime();
            var endTime = startTime + duration;
            var totalPoints = path.length;

            // 每隔一段时间更新标记的位置
            var timer = setInterval(function() {
                var now = new Date().getTime();
                var fraction = (now - startTime) / duration;
                if (fraction >= 1) {
                    clearInterval(timer);
                }
                // 计算当前路径点的索引
                var currentIndex = Math.floor(fraction * totalPoints);
                // 如果路径点索引发生变化，则更新标记位置
                if (currentIndex !== index) {
                    index = currentIndex;
                    marker.setPosition(path[index]);
                }
            }, 7);
        }
    }

    distanceBox = document.getElementById("run_distance");
    schoolSiteBox = document.getElementById("school_site");
    distanceBox.addEventListener("blur", function(){
        if (distanceBox.value > 0 && distanceBox.value != distance) {
            distance = distanceBox.value;
            school_site = schoolSiteBox.value;
            // console.log("Distance: " + distance);
            sendAndDisplay(distance, school_site);
        }
    });

    schoolSiteBox.addEventListener("change", function(){
        if (distanceBox.value > 0) {
            distance = distanceBox.value;
            school_site = schoolSiteBox.value;
            // console.log("Distance: " + distanceBox.value);
            // console.log("School Site: " + school_site);
            sendAndDisplay(distance, school_site);
        }
    });
    

    randTackButton = document.getElementById("rand-tack-btn");
    randTackButton.addEventListener("click", function(){
        if (distanceBox.value > 0) {
            sendAndDisplay(distance, school_site);
        }
    });

    submitButton = document.getElementById("submit-btn");
    submitButton.addEventListener("click", function(){
        var formData = {
            "phone": document.getElementById("phone").value,
            "password": document.getElementById("password").value,
            "run_distance": document.getElementById("run_distance").value,
            "run_time": document.getElementById("run_time").value,
            "school_site": document.getElementById("school_site").value,
            "track": track,
        };
    
        fetch('/autoRun', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.code == "10000") {
                alert(data['msg']);
            } else {
                alert(data['msg']);
            }
            // 这里可以根据返回的数据执行其他操作
        })
        .catch((error) => {
            alert("提交失败");
            console.error('Error:', error);
        });
    });
    
};








