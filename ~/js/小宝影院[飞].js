muban.首图.二级.title = 'h1&&Text;.data--span:eq(0)&&Text';
muban.首图.二级.desc = '#score&&Text;;;.data--span:eq(2)&&Text;.data--span:eq(3)&&Text';
var rule={
	title:'小宝影院[飞]',
	模板:'首图',
	host:'https://xiaobaotv.net',
	url:'/index.php/vod/show/id/fyfilter.html',
	filterable:1,//是否启用分类筛选,
	filter_url:'{{fl.cateId}}{{fl.area}}{{fl.by}}{{fl.class}}{{fl.lang}}/page/fypage{{fl.year}}',
	filter: {
		"7":[{"key":"cateId","name":"类型","value":[{"n":"全部","v":"7"},{"n":"喜剧片","v":"24"},{"n":"冒险片","v":"25"},{"n":"剧情片","v":"26"},{"n":"动作片","v":"27"},{"n":"网络电影","v":"39"},{"n":"同性片","v":"29"},{"n":"奇幻片","v":"30"},{"n":"恐怖片","v":"31"},{"n":"悬疑片","v":"32"},{"n":"惊悚片","v":"50"},{"n":"歌舞片","v":"33"},{"n":"灾难片","v":"34"},{"n":"爱情片","v":"35"},{"n":"犯罪片","v":"36"},{"n":"科幻片","v":"37"},{"n":"经典片","v":"38"},{"n":"动画电影","v":"28"},{"n":"战争片","v":"40"}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"🇨🇳中国","v":"/area/大陆"},{"n":"🇭🇰香港","v":"/area/香港"},{"n":"🇹🇼台湾","v":"/area/台湾"},{"n":"🇯🇵日本","v":"/area/日本"},{"n":"🇰🇷韩国","v":"/area/韩国"},{"n":"欧美","v":"/area/欧美"},{"n":"泰国","v":"/area/泰国"},{"n":"新马","v":"/area/新马"},{"n":"其它","v":"/area/其它"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2025","v":"/year/2025"},{"n":"2024","v":"/year/2024"},{"n":"2023","v":"/year/2023"},{"n":"2022","v":"/year/2022"},{"n":"2021","v":"/year/2021"},{"n":"2020","v":"/year/2020"},{"n":"2019","v":"/year/2019"},{"n":"2018","v":"/year/2018"},{"n":"2017","v":"/year/2017"},{"n":"2016","v":"/year/2016"},{"n":"2015","v":"/year/2015"},{"n":"2014","v":"/year/2014"},{"n":"2013","v":"/year/2013"},{"n":"2012","v":"/year/2012"},{"n":"2011","v":"/year/2011"},{"n":"2010","v":"/year/2010"},{"n":"2009","v":"/year/2009"},{"n":"2008","v":"/year/2008"},{"n":"2007","v":"/year/2007"},{"n":"2006","v":"/year/2006"},{"n":"2005","v":"/year/2005"},{"n":"2004","v":"/year/2004"}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"/lang/国语"},{"n":"英语","v":"/lang/英语"},{"n":"粤语","v":"/lang/粤语"},{"n":"韩语","v":"/lang/韩语"},{"n":"日语","v":"/lang/日语"},{"n":"法语","v":"/lang/法语"},{"n":"德语","v":"/lang/德语"},{"n":"西班牙","v":"/lang/西班牙"},{"n":"意大利","v":"/lang/意大利"},{"n":"泰国语","v":"/lang/泰国语"},{"n":"其它","v":"/lang/其它"}]},{"key":"by","name":"排序","value":[{"n":"时间","v":"/by/time"},{"n":"人气","v":"/by/hits"},{"n":"评分","v":"/by/score"}]}],
		"6":[{"key":"cateId","name":"类型","value":[{"n":"全部","v":"6"},{"n":"国产剧","v":"41"},{"n":"港剧","v":"42"},{"n":"台剧","v":"43"},{"n":"日剧","v":"44"},{"n":"韩剧","v":"45"},{"n":"欧美剧","v":"46"},{"n":"泰剧","v":"47"},{"n":"新马剧","v":"48"},{"n":"其他剧","v":"49"}]},{"key":"class","name":"分类","value":[{"n":"全部","v":""},{"n":"偶像","v":"/class/电视剧-偶像"},{"n":"爱情","v":"/class/电视剧-爱情"},{"n":"言情","v":"/class/电视剧-言情"},{"n":"古装","v":"/class/电视剧-古装"},{"n":"历史","v":"/class/电视剧-历史"},{"n":"玄幻","v":"/class/电视剧-玄幻"},{"n":"谍战","v":"/class/电视剧-谍战"},{"n":"历险","v":"/class/电视剧-历险"},{"n":"都市","v":"/class/电视剧-都市"},{"n":"科幻","v":"/class/电视剧-科幻"},{"n":"军旅","v":"/class/电视剧-军旅"},{"n":"喜剧","v":"/class/电视剧-喜剧"},{"n":"武侠","v":"/class/电视剧-武侠"},{"n":"江湖","v":"/class/电视剧-江湖"},{"n":"罪案","v":"/class/电视剧-罪案"},{"n":"青春","v":"/class/电视剧-青春"},{"n":"家庭","v":"/class/电视剧-家庭"},{"n":"战争","v":"/class/电视剧-战争"},{"n":"悬疑","v":"/class/电视剧-悬疑"},{"n":"穿越","v":"/class/电视剧-穿越"},{"n":"宫廷","v":"/class/电视剧-宫廷"},{"n":"神话","v":"/class/电视剧-神话"},{"n":"商战","v":"/class/电视剧-商战"},{"n":"警匪","v":"/class/电视剧-警匪"},{"n":"动作","v":"/class/电视剧-动作"},{"n":"惊悚","v":"/class/电视剧-惊悚"},{"n":"剧情","v":"/class/电视剧-剧情"},{"n":"同性","v":"/class/电视剧-同性"},{"n":"奇幻","v":"/class/电视剧-奇幻"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2025","v":"/year/2025"},{"n":"2024","v":"/year/2024"},{"n":"2023","v":"/year/2023"},{"n":"2022","v":"/year/2022"},{"n":"2021","v":"/year/2021"},{"n":"2020","v":"/year/2020"},{"n":"2019","v":"/year/2019"},{"n":"2018","v":"/year/2018"},{"n":"2017","v":"/year/2017"},{"n":"2016","v":"/year/2016"},{"n":"2015","v":"/year/2015"},{"n":"2014","v":"/year/2014"},{"n":"2013","v":"/year/2013"},{"n":"2012","v":"/year/2012"},{"n":"2011","v":"/year/2011"},{"n":"2010","v":"/year/2010"},{"n":"2009","v":"/year/2009"},{"n":"2008","v":"/year/2008"},{"n":"2007","v":"/year/2007"},{"n":"2006","v":"/year/2006"},{"n":"2005","v":"/year/2005"},{"n":"2004","v":"/year/2004"}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"/lang/国语"},{"n":"粤语","v":"/lang/粤语"},{"n":"英语","v":"/lang/英语"},{"n":"韩语","v":"/lang/韩语"},{"n":"日语","v":"/lang/日语"},{"n":"西班牙","v":"/lang/西班牙"},{"n":"法语","v":"/lang/法语"},{"n":"德语","v":"/lang/德语"},{"n":"意大利","v":"/lang/意大利"},{"n":"泰国语","v":"/lang/泰国语"},{"n":"其它","v":"/lang/其它"}]},{"key":"by","name":"排序","value":[{"n":"时间","v":"/by/time"},{"n":"人气","v":"/by/hits"},{"n":"评分","v":"/by/score"}]}],
		"3":[{"key":"cateId","name":"类型","value":[{"n":"全部","v":"3"},{"n":"国产综艺","v":"57"},{"n":"港台综艺","v":"58"},{"n":"日本综艺","v":"59"},{"n":"韩国综艺","v":"60"},{"n":"欧美综艺","v":"61"},{"n":"新马泰综艺","v":"62"},{"n":"其他综艺","v":"63"}]},{"key":"class","name":"分类","value":[{"n":"全部","v":""},{"n":"真人秀","v":"综艺-真人秀"},{"n":"选秀","v":"综艺-选秀"},{"n":"网综","v":"综艺-网综"},{"n":"脱口秀","v":"综艺-脱口秀"},{"n":"搞笑","v":"综艺-搞笑"},{"n":"竞技","v":"综艺-竞技"},{"n":"情感","v":"综艺-情感"},{"n":"访谈","v":"综艺-访谈"},{"n":"演唱会","v":"综艺-演唱会"},{"n":"晚会","v":"综艺-晚会"},{"n":"其它","v":"综艺-其它"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2025","v":"/year/2025"},{"n":"2024","v":"/year/2024"},{"n":"2023","v":"/year/2023"},{"n":"2022","v":"/year/2022"},{"n":"2021","v":"/year/2021"},{"n":"2020","v":"/year/2020"},{"n":"2019","v":"/year/2019"},{"n":"2018","v":"/year/2018"},{"n":"2017","v":"/year/2017"},{"n":"2016","v":"/year/2016"},{"n":"2015","v":"/year/2015"},{"n":"2014","v":"/year/2014"},{"n":"2013","v":"/year/2013"},{"n":"2012","v":"/year/2012"},{"n":"2011","v":"/year/2011"},{"n":"2010","v":"/year/2010"},{"n":"2009","v":"/year/2009"},{"n":"2008","v":"/year/2008"},{"n":"2007","v":"/year/2007"},{"n":"2006","v":"/year/2006"},{"n":"2005","v":"/year/2005"},{"n":"2004","v":"/year/2004"}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"/lang/国语"},{"n":"粤语","v":"/lang/粤语"},{"n":"英语","v":"/lang/英语"},{"n":"韩语","v":"/lang/韩语"},{"n":"日语","v":"/lang/日语"},{"n":"西班牙","v":"/lang/西班牙"},{"n":"法语","v":"/lang/法语"},{"n":"德语","v":"/lang/德语"},{"n":"意大利","v":"/lang/意大利"},{"n":"泰国语","v":"/lang/泰国语"},{"n":"其它","v":"/lang/其它"}]},{"key":"by","name":"排序","value":[{"n":"时间","v":"/by/time"},{"n":"人气","v":"/by/hits"},{"n":"评分","v":"/by/score"}]}],
		"5":[{"key":"cateId","name":"类型","value":[{"n":"全部","v":"5"},{"n":"国产动漫","v":"51"},{"n":"日本动漫","v":"52"},{"n":"港台动漫","v":"53"},{"n":"欧美动漫","v":"54"},{"n":"韩国动漫","v":"55"},{"n":"新马泰动漫","v":"56"}]},{"key":"class","name":"分类","value":[{"n":"全部","v":""},{"n":"热血","v":"动漫-热血"},{"n":"格斗","v":"动漫-格斗"},{"n":"机战","v":"动漫-机战"},{"n":"少女","v":"动漫-少女"},{"n":"竞技","v":"动漫-竞技"},{"n":"科幻","v":"动漫-科幻"},{"n":"魔幻","v":"动漫-魔幻"},{"n":"爆笑","v":"动漫-爆笑"},{"n":"推理","v":"动漫-推理"},{"n":"冒险","v":"动漫-冒险"},{"n":"恋爱","v":"动漫-恋爱"},{"n":"校园","v":"动漫-校园"},{"n":"治愈","v":"动漫-治愈"},{"n":"泡面","v":"动漫-泡面"},{"n":"穿越","v":"动漫-穿越"},{"n":"灵异","v":"动漫-灵异"},{"n":"耽美","v":"动漫-耽美"},{"n":"动画电影","v":"动漫-动画电影"},{"n":"其它","v":"动漫-其它"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2025","v":"/year/2025"},{"n":"2024","v":"/year/2024"},{"n":"2023","v":"/year/2023"},{"n":"2022","v":"/year/2022"},{"n":"2021","v":"/year/2021"},{"n":"2020","v":"/year/2020"},{"n":"2019","v":"/year/2019"},{"n":"2018","v":"/year/2018"},{"n":"2017","v":"/year/2017"},{"n":"2016","v":"/year/2016"},{"n":"2015","v":"/year/2015"},{"n":"2014","v":"/year/2014"},{"n":"2013","v":"/year/2013"},{"n":"2012","v":"/year/2012"},{"n":"2011","v":"/year/2011"},{"n":"2010","v":"/year/2010"},{"n":"2009","v":"/year/2009"},{"n":"2008","v":"/year/2008"},{"n":"2007","v":"/year/2007"},{"n":"2006","v":"/year/2006"},{"n":"2005","v":"/year/2005"},{"n":"2004","v":"/year/2004"}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"/lang/国语"},{"n":"粤语","v":"/lang/粤语"},{"n":"英语","v":"/lang/英语"},{"n":"韩语","v":"/lang/韩语"},{"n":"日语","v":"/lang/日语"},{"n":"西班牙","v":"/lang/西班牙"},{"n":"法语","v":"/lang/法语"},{"n":"德语","v":"/lang/德语"},{"n":"意大利","v":"/lang/意大利"},{"n":"泰国语","v":"/lang/泰国语"},{"n":"其它","v":"/lang/其它"}]},{"key":"by","name":"排序","value":[{"n":"时间","v":"/by/time"},{"n":"人气","v":"/by/hits"},{"n":"评分","v":"/by/score"}]}],
		"21":[{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"🇨🇳中国","v":"/area/大陆"},{"n":"🇭🇰香港","v":"/area/香港"},{"n":"🇹🇼台湾","v":"/area/台湾"},{"n":"🇯🇵日本","v":"/area/日本"},{"n":"🇰🇷韩国","v":"/area/韩国"},{"n":"欧美","v":"/area/欧美"},{"n":"泰国","v":"/area/泰国"},{"n":"新马","v":"/area/新马"},{"n":"其它","v":"/area/其它"}]},{"key":"class","name":"分类","value":[{"n":"全部","v":""},{"n":"文化","v":"纪录片-文化"},{"n":"探索","v":"纪录片-探索"},{"n":"军事","v":"纪录片-军事"},{"n":"解密","v":"纪录片-解密"},{"n":"科技","v":"纪录片-科技"},{"n":"历史","v":"纪录片-历史"},{"n":"人物","v":"纪录片-人物"},{"n":"自然","v":"纪录片-自然"},{"n":"其它","v":"纪录片-其它"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2025","v":"/year/2025"},{"n":"2024","v":"/year/2024"},{"n":"2023","v":"/year/2023"},{"n":"2022","v":"/year/2022"},{"n":"2021","v":"/year/2021"},{"n":"2020","v":"/year/2020"},{"n":"2019","v":"/year/2019"},{"n":"2018","v":"/year/2018"},{"n":"2017","v":"/year/2017"},{"n":"2016","v":"/year/2016"},{"n":"2015","v":"/year/2015"},{"n":"2014","v":"/year/2014"},{"n":"2013","v":"/year/2013"},{"n":"2012","v":"/year/2012"},{"n":"2011","v":"/year/2011"},{"n":"2010","v":"/year/2010"},{"n":"2009","v":"/year/2009"},{"n":"2008","v":"/year/2008"},{"n":"2007","v":"/year/2007"},{"n":"2006","v":"/year/2006"},{"n":"2005","v":"/year/2005"},{"n":"2004","v":"/year/2004"}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"/lang/国语"},{"n":"粤语","v":"/lang/粤语"},{"n":"英语","v":"/lang/英语"},{"n":"韩语","v":"/lang/韩语"},{"n":"日语","v":"/lang/日语"},{"n":"西班牙","v":"/lang/西班牙"},{"n":"法语","v":"/lang/法语"},{"n":"德语","v":"/lang/德语"},{"n":"意大利","v":"/lang/意大利"},{"n":"泰国语","v":"/lang/泰国语"},{"n":"其它","v":"/lang/其它"}]},{"key":"by","name":"排序","value":[{"n":"时间","v":"/by/time"},{"n":"人气","v":"/by/hits"},{"n":"评分","v":"/by/score"}]}],
		"20":[{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"🇨🇳中国","v":"/area/大陆"},{"n":"🇭🇰香港","v":"/area/香港"},{"n":"🇹🇼台湾","v":"/area/台湾"},{"n":"🇯🇵日本","v":"/area/日本"},{"n":"🇰🇷韩国","v":"/area/韩国"},{"n":"欧美","v":"/area/欧美"},{"n":"泰国","v":"/area/泰国"},{"n":"新马","v":"/area/新马"},{"n":"其它","v":"/area/其它"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2025","v":"/year/2025"},{"n":"2024","v":"/year/2024"},{"n":"2023","v":"/year/2023"},{"n":"2022","v":"/year/2022"},{"n":"2021","v":"/year/2021"},{"n":"2020","v":"/year/2020"},{"n":"2019","v":"/year/2019"},{"n":"2018","v":"/year/2018"},{"n":"2017","v":"/year/2017"},{"n":"2016","v":"/year/2016"},{"n":"2015","v":"/year/2015"},{"n":"2014","v":"/year/2014"},{"n":"2013","v":"/year/2013"},{"n":"2012","v":"/year/2012"},{"n":"2011","v":"/year/2011"},{"n":"2010","v":"/year/2010"},{"n":"2009","v":"/year/2009"},{"n":"2008","v":"/year/2008"},{"n":"2007","v":"/year/2007"},{"n":"2006","v":"/year/2006"},{"n":"2005","v":"/year/2005"},{"n":"2004","v":"/year/2004"}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"/lang/国语"},{"n":"粤语","v":"/lang/粤语"},{"n":"英语","v":"/lang/英语"},{"n":"韩语","v":"/lang/韩语"},{"n":"日语","v":"/lang/日语"},{"n":"西班牙","v":"/lang/西班牙"},{"n":"法语","v":"/lang/法语"},{"n":"德语","v":"/lang/德语"},{"n":"意大利","v":"/lang/意大利"},{"n":"泰国语","v":"/lang/泰国语"},{"n":"其它","v":"/lang/其它"}]},{"key":"by","name":"排序","value":[{"n":"时间","v":"/by/time"},{"n":"人气","v":"/by/hits"},{"n":"评分","v":"/by/score"}]}]
	},
	filter_def:{
		7:{cateId:'7',by:'/by/time'},
		6:{cateId:'6',by:'/by/time'},
		3:{cateId:'3',by:'/by/time'},
		5:{cateId:'5',by:'/by/time'},
		21:{cateId:'21',by:'/by/time'},
		20:{cateId:'20',by:'/by/time'}
	},
	searchUrl:'/index.php/vod/search.html?wd=**',
	class_parse:'.myui-header__menu&&li.hidden-xs:gt(0):lt(7);a&&Text;a&&href;./(\\d+).html',
    lazy:`js:
        var html = JSON.parse(request(input).match(/r player_.*?=(.*?)</)[1]);
        var url = html.url;
        if (html.encrypt == '1') {
            url = unescape(url)
        } else if (html.encrypt == '2') {
            url = unescape(base64Decode(url))
        }
        if (/m3u8|mp4/.test(url)) {
            input = url
        } else {
            input
        }
    `,
}