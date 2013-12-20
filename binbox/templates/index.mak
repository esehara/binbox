<!DOCTYPE HTML>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>BinBox</title>
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
	<link rel="stylesheet" href="${request.static_url("binbox:static/main.css")}" />
	<script type="text/javascript">
	$(document).ready(function(){
		
		$.getJSON("json/list", function(json) {
			file_max = json.length;
			
			for (var i = 0; i < file_max; i ++) {
				$.getJSON("json/file?target=" + json[i], function(filename) {
					if (filename[0]) {
						var img_tag = $('<img>').attr('src', filename[1]);
						var a_tag = $('<a>').attr('href', filename[2]);
						a_tag.prepend(img_tag);
						$('div#test').prepend(a_tag);
					}
				});
			}
			
		});

	});
	</script>
</head>
<body>
        <h1>BinBox</h1>
		<h2>for Poor Books</h2>
		<div id="nav">
			<a href="list">文字表示</a>　｜　<a href=".">画像表示</a>
		</div>
		<form action="post" method="POST" enctype="multipart/form-data">
			<input name="pdf" type="file" value="" />
			<input type="submit" value="submit" />
		</form>
% if mode == "thumb":
	<div id="test">
	</div>
% endif
% if mode == "list":
<ul>
		% for book in books:
		<li>
			<a href="${request.static_url(book.get_filepath())}">
        		${book.view_name()}
			</a>
		</li>
		% endfor
</ul>
% endif 
</body>
</html>
