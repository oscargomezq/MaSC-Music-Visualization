import numpy as np
import pandas as pd
import os
import plotly.express as px
import plotly
from bokeh.layouts import row, gridplot, layout
from bokeh.models import CustomJS, ColumnDataSource, HoverTool, TapTool, WheelZoomTool, LassoSelectTool, BoxSelectTool, PanTool, HelpTool
from bokeh.plotting import figure, output_file, show
from utils import save_params, check_repeated_params, unpack_params, user_confirmation

# Create 2d visualization on the dataset and clusters given
# Loads data set from dataset_path and the labels from clustering_path
# Saves visualization to save_to_path as HTML
# Takes in the kwargs used for the experiment (sr, hop_length, etc.)
def bokeh_2d(save_to, load_from_data, load_from_clusters, audio_path, **curr_params_data):
	
	df_data = pd.read_csv(load_from_data, names=['UniqueID', 'f1', 'f2'])
	df_clusters = pd.read_csv(load_from_clusters, names=['UniqueID', 'label'])
	df_plot = df_data.join(df_clusters.set_index('UniqueID'), on='UniqueID')

	uid = df_plot['UniqueID'].values
	x = df_plot['f1'].values
	y = df_plot['f2'].values
	label = df_plot['label'].values

	color_vals = ["olive", "darkred", "goldenrod", "skyblue", "red", "darkblue", "gray", "indigo", "black"]
	color = np.array([color_vals[l] for l in label])
	audio = np.array([os.path.join(audio_path, iD + '.wav') for iD in uid])
	images = np.array([])

	# output_file(save_to)

	s1 = ColumnDataSource(data = dict(x=x, y=y,
						  desc=audio, #arts=artists, imgs=images, dsp=display_names,
						  colors=color))
    
	hover = HoverTool(tooltips="""
	    <div>
	    	// Make an id for the div
	    	// Insert JS code that evaluates if it is the first element of its type and decide if append the img and audio src or not
	        <img
	            src="@imgs" height="120" alt="@imgs" width="120" style="display: block; margin-left: auto; margin-right: auto;"
	            border="2"
	        ></img>
	    </div>
	    <div>
	        <p align="center">@dsp</p>
	    </div>
	    <div>
	        <audio
	            src="@desc" height="20" width="20" autoplay 
	            border="2"
	        ></audio>
	    </div>
	    """
	)

	taptoolcallback = CustomJS(args = dict(source=s1), code = """

		var names = source.data['desc'];
	    var inds = source['selected']['1d'].indices;

	    for (i=0; i<inds.length; i++){

	        var title = names[inds[i]];

	        var para = document.createElement("p");
	        var node = document.createTextNode(title);
	        para.appendChild(node);
	        document.body.appendChild(para);

	        var x = document.createElement("AUDIO");
	        var song = String(title);
	        x.setAttribute("src",song);
	        x.setAttribute("controls", "controls");

	        document.body.appendChild(x);

	        var para2 = document.createElement("br");
	        document.body.appendChild(para2);

	    }   
		"""
	)
	tap = TapTool(callback = taptoolcallback)

	boxtoolcallback = CustomJS(args=dict(source=s1),code = """

	    var names = source.data['desc'];
	    var inds = source['selected']['1d'].indices;

	    for (i=0; i<inds.length; i++){

	        var title = names[inds[i]];

	        var para = document.createElement("p");
	        var node = document.createTextNode(title);
	        para.appendChild(node);
	        document.body.appendChild(para);

	        var x = document.createElement("AUDIO");
	        var song = String(title);
	        x.setAttribute("src",song);
	        x.setAttribute("controls", "controls");

	        document.body.appendChild(x);

	        var para2 = document.createElement("br");
	        document.body.appendChild(para2);

	    }
	    
		"""
	)
	box = BoxSelectTool(callback = boxtoolcallback)

	help_b = HelpTool(help_tooltip = """
	    Button fuctions:\n

	    Pan: Move around plot\n
	    Lasso Select: View plot of artists in selection\n
	    Box Select: Listen to all songs in selection\n
	    Wheel Zoom: Resize plot\n
	    Tap (Click): Listen to all overlaping songs\n
	    Hover: Listen, view album cover and title\n
	    Reset\n
	    """
	)

	wheel_zoom = WheelZoomTool()
	lasso_select = LassoSelectTool()

	p2 = figure(width = 700, height = 700)
	p1 = figure(tools=[hover, tap, box, lasso_select, help_b, wheel_zoom, "pan", "reset"],
		        toolbar_location="right", toolbar_sticky=False,
		        title="Music Collections", width = 700, height = 700)

	p1.circle('x', 'y', source=s1, size=7.3, fill_alpha = 0.5, fill_color = 'colors', line_color = 'colors')
	p1.title.text_font_size = '12pt'
	p1.title.align = 'center'
	p1.toolbar.active_scroll = wheel_zoom
	p1.toolbar.active_drag = lasso_select

	s2 = ColumnDataSource(data=dict(artists=[], counts=[], full_artists=[], full_counts=[]))

	# s1.callback = CustomJS(args=dict(s2=s2), code="""

	# 	console.log(cb_obj);

	#     var inds = cb_obj.selected['1d'].indices;
	#     var d1 = cb_obj.data;
	#     var d2 = s2.data;
	#     d2['full_artists'] = [];
	#     d2['full_counts'] = [];
	#     var max_freq = 0;

	#     for (i=0; i<inds.length; i++){

	#         var current = d1['arts'][inds[i]];

	#         if (d2['full_artists'].indexOf(current) == -1){
	#             d2['full_artists'].push(d1['arts'][inds[i]]);
	#             d2['full_counts'].push(1);
	#         }
	#         else{
	#             d2['full_counts'][d2['full_artists'].indexOf(current)] += 1;
	#             if (d2['full_counts'][d2['full_artists'].indexOf(current)] > max_freq){
	#             	max_freq = d2['full_counts'][d2['full_artists'].indexOf(current)];
	#             }
	#         }
	        
	#     }

	#     console.log(max_freq);

	#     d2['artists'] = [];
	#     d2['counts'] = [];
	#     var thres = max_freq * 0.05;

	#     //filter arrays to only include freqs >= 5pcnt of max_freq

	#     for (i=0; i<d2['full_artists'].length; i++){

	#     	if (d2['full_counts'][i] >= thres){
	#     		d2['artists'].push(d2['full_artists'][i]);
	#     		d2['counts'].push(d2['full_counts'][i]);
	#     	}

	#     }


	#     s2.change.emit();

	#     if (inds.length > 5){


	#         if (document.getElementById("right_side_style")==null){
	#             var css = ".right_side div {\\n\\tfont: 12px sans-serif;\\n";
	#             css = css.concat("\\tbackground-color: white;\\n\\tpadding: 3px;\\n\\tcolor: white;}");
	#             var style = document.createElement('style');
	#             style.type = 'text/css';
	#             style.id = "right_side_style";
	#             style.appendChild(document.createTextNode(css));
	#             document.head.appendChild(style);
	#         }

	#         if (document.getElementById("chart_style")==null){
	#             var css = ".chart div {\\n\\tfont: 12px sans-serif;\\n";
	#             css = css.concat("\\tbackground-color: steelblue;\\n\\topacity: 0.8;\\n\\theight: 14px;\\n\\tmargin: 1px;\\n\\twidth: 470px;\\n\\ttext-align: right;\\n\\tcolor: white;}");
	#             var style = document.createElement('style');
	#             style.type = 'text/css';
	#             style.id = "chart_style";
	#             style.appendChild(document.createTextNode(css));
	#             document.head.appendChild(style);
	#         }

	#         if (document.getElementById("artist_style")==null){
	#             var css = ".artists div {\\n\\tfont: 12px sans-serif;\\n";
	#             css = css.concat("\\tbackground-color: white;\\n\\theight: 14px;\\n\\tmargin: 1px;\\n\\twidth: 470px;\\n\\ttext-align: right;\\n\\tcolor: black;}");
	#             var style = document.createElement('style');
	#             style.type = 'text/css';
	#             style.id = "artist_style";
	#             style.appendChild(document.createTextNode(css));
	#             document.head.appendChild(style);
	#         }

	#         if (document.getElementById("right_side_div")==null){
	#             var rightdiv = document.createElement('div');
	#             rightdiv.className = "right_side";
	#             rightdiv.style = "float: left; tdisplay: inline-flex; width: 970px;";
	#             rightdiv.id = "right_side_div";
	#             document.getElementsByClassName("bk-spacer-box bk-layout-fixed")[0].innerHTML = "";
	#             document.getElementsByClassName("bk-spacer-box bk-layout-fixed")[0].style = "width: 970px";
	#             document.getElementsByClassName("bk-spacer-box bk-layout-fixed")[0].appendChild(rightdiv);
	#         }
	#         else{
	#         	document.getElementsByClassName("bk-spacer-box bk-layout-fixed")[0].style = "width: 970px";
	#             document.getElementById("right_side_div").innerHTML = "";
	#         }

	#         if (document.getElementById("title_p")==null){
	#             var para = document.createElement("p");
	#             var node = document.createTextNode("Artist Frequencies");
	#             para.className = "title";
	#             para.style = "text-align: center; font-weight: bold; font-size: 15px;";
	#             para.id = "title_p";
	#             para.appendChild(node);
	#             document.getElementsByClassName("right_side")[0].appendChild(para);
	#         }
	#         else{
	#             document.getElementById("artists_div").innerHTML = "";
	#         }

	#         if (document.getElementById("artists_div")==null){
	#             var artdiv = document.createElement('div');
	#             artdiv.className = "artists";
	#             artdiv.style = "float: left; tdisplay: inline-flex;";
	#             artdiv.id = "artists_div";
	#             document.getElementsByClassName("right_side")[0].appendChild(artdiv);
	#         }
	#         else{
	#             document.getElementById("artists_div").innerHTML = "";
	#         }

	#         if (document.getElementById("chart_div")==null){
	#             var chartdiv = document.createElement('div');
	#             chartdiv.className = "chart";
	#             chartdiv.style = "float: right; tdisplay: inline-flex;";
	#             chartdiv.id = "chart_div";
	#             document.getElementsByClassName("right_side")[0].appendChild(chartdiv);
	#         }
	#         else{
	#             document.getElementById("chart_div").innerHTML = "";
	#         }


	#         if (document.getElementById("source_d3js")==null){
	#             var d3js = document.createElement('script');
	#             d3js.src = "https://d3js.org/d3.v3.min.js";
	#             d3js.id = "source_d3js";
	#             document.body.appendChild(d3js);
	#         }


	#         if (document.getElementById("mycode")==null){
	#             var code_div = document.createElement('script');
	#             code_div.id = "mycode";
	#             document.body.appendChild(code_div);
	#         }

	#         //populate var data with d2["counts"] and var art_names with d2["artists"]

	#         var string = "[";

	#         for (j=0; j<d2['counts'].length-1; j++){
	#         	var tmp = d2['counts'][j];
	#             string = string.concat(tmp);
	#             string += ", ";
	#         }
	        
	#         var tmp = d2['counts'][d2['counts'].length-1];
	#         string = string.concat(tmp);
	#         string += "]";


	#         var string1 = "[\\"";

	#         for (j=0; j<d2['artists'].length-1; j++){
	#             var tmp = d2['artists'][j];
	#             string1 = string1.concat(tmp);
	#             string1 = string1.concat("\\"")
	#             string1 += ", \\"";
	#         }
	        
	#         var tmp = d2['artists'][d2['artists'].length-1];
	#         string1 = string1.concat(tmp);
	#         string1 += "\\"]";


	#         var d3js_code = "var data = ";
	#         d3js_code = d3js_code.concat(string);
	#         d3js_code = d3js_code + ";\\n\\n";

	#         d3js_code = d3js_code+ "var art_names = ";
	#         d3js_code = d3js_code.concat(string1);
	#         d3js_code = d3js_code + ";\\n\\n";


	#         d3js_code = d3js_code.concat("var x = d3.scale.linear()\\n    .domain([0, d3.max(data)])\\n    .range([0, 470]);\\n\\n");
	#         //    var x = d3.scale.linear()
	#         //        .domain([0, d3.max(data)])
	#         //        .range([0, 420]);

	        
	#         d3js_code = d3js_code.concat("d3.select(\\".chart\\")\\n  .selectAll(\\"div\\")\\n    "+
	#         ".data(data)\\n  .enter().append(\\"div\\")\\n    "+
	#         ".style(\\"width\\", function(d) { return x(d) + \\"px\\"; })\\n    .text(function(d) { return d; });");

	#         //    d3.select(".chart")
	#         //      .selectAll("div")
	#         //        .data(data)
	#         //      .enter().append("div")
	#         //        .style("width", function(d) { return x(d) + "px"; })
	#         //        .style("margin", "auto 5px")
	#         //        .text(function(d) { return d; });";
	#         //        .class("chartel");


	        
	#         d3js_code = d3js_code.concat("\\n\\nd3.select(\\".artists\\")\\n  .selectAll(\\"div\\")\\n    "+
	#         ".data(art_names)\\n  .enter().append(\\"div\\")\\n    "+
	#         ".style(\\"width\\", \\"300\\")\\n    .text(function(d) { return d; });");

	#         //    d3.select(".artists")
	#         //      .selectAll("div")
	#         //        .data(art_names)
	#         //      .enter().append("div")
	#         //        .style("width", "300")
	#         //        .style("margin", "auto 5px")
	#         //        .text(function(d) { return d; });";
	#         //        .class("artel");

	#         document.getElementById("mycode").innerHTML = "";
	#         document.getElementById("mycode").appendChild(document.createTextNode(d3js_code));


	          
	#         var script = document.getElementById("mycode");
	        
	#         eval(script.innerHTML);


	#         // Check if chart and script exist
	#         // if not, create them
	#         // if they are, change innerhtml for script
	#         // delete nodes from char and repopulate with new data    

	#     }

	#     """
	# )

	grid = gridplot([[p1, None]], merge_tools=False)
	show(grid)

# Create 3d visualization on the dataset and clusters given
# Loads data set from dataset_path and the labels from clustering_path
# Saves visualization to save_to_path as HTML
# Takes in the kwargs used for the experiment (sr, hop_length, etc.)
def plotly_3d(save_to, load_from_data, load_from_clusters, audio_path, **curr_params_data):
	
	df_data = pd.read_csv(load_from_data, names=['UniqueID', 'f1', 'f2', 'f3'])
	df_clusters = pd.read_csv(load_from_clusters, names=['UniqueID', 'label'])
	df_plot = df_data.join(df_clusters.set_index('UniqueID'), on='UniqueID')

	fig = px.scatter_3d(df_plot, x='f1', y='f2', z='f3', color='label')
	plotly.io.write_html(fig, file=save_to, auto_open=False)
	

# Perform 2d or 3d visualization on the dataset given with the clustering labels given
# params_path is a list with paths to where the parameters for preprocessing, feature extraction, etc. are stored
# params_list_data is the combination of parameters for the dataset to use
# params_list_clusters is the combination of parameters for the cluster labels to use
def perform_visualization(params_path_data, params_path_clusters, params_list_data, params_list_clusters, audio_path):

	curr_params_data = unpack_params(params_path_data, params_list_data)
	curr_params_clusters = unpack_params(params_path_clusters, params_list_clusters)

	dim = curr_params_data['components']

	save_to = '2D_visualization_labels' if dim == 2 else ('3D_visualization_labels' if dim == 3 else 'invalid')
	save_to += '_(' + str(params_list_clusters[0])
	for i in params_list_clusters[1:-1]:
		save_to += '_' + str(i)
	save_to += ')_' + str(params_list_clusters[-1])
	save_to += '_data_(' + str(params_list_data[0])
	for i in params_list_data[1:]:
		save_to += '_' + str(i)
	save_to += ').html'
	save_to = os.path.join('visualizations', save_to)

	load_from_data = 'small_dataset'
	for i in params_list_data:
		load_from_data += '_' + str(i)
	load_from_data += '.csv'
	load_from_data = os.path.join(params_path_data[-1], load_from_data)

	load_from_clusters = 'cluster_labels'
	load_from_clusters += '_(' + str(params_list_clusters[0])
	for i in params_list_clusters[1:-1]:
		load_from_clusters += '_' + str(i)
	load_from_clusters += ')_' + str(params_list_clusters[-1])
	load_from_clusters += '.csv'	
	load_from_clusters = os.path.join(params_path_clusters[-1], load_from_clusters)


	print("Creating visualization...")
	print("Using dataset parameters: " + str(curr_params_data))
	print("Using clustering parameters: " + str(curr_params_clusters))
	print("Saving at: " + save_to)
	print("Loading dataset from: " + load_from_data)
	print("Loading clusters from: " + load_from_clusters)

	if os.path.exists(save_to):
		print ("Clustering for these parameters already done!")
		return

	# Create visualization using the preferred parameters
	if dim == 2:
		bokeh_2d(save_to, load_from_data, load_from_clusters, audio_path, **curr_params_data)
	elif dim == 3:
		plotly_3d(save_to, load_from_data, load_from_clusters, audio_path, **curr_params_data)


if __name__ == "__main__":

    # Local folders for preprocessing parameters
    preproc_path = 'preprocessing'
    feature_ext_path = 'full_datasets'
    mid_dim_path = 'mid_datasets'
    small_dim_path = 'small_datasets'
    clustering_path = 'clustering_labels'
    params_path_data = [preproc_path, feature_ext_path, mid_dim_path, small_dim_path]
    params_path_clusters = [preproc_path, feature_ext_path, clustering_path]
    
    # Define the sets of parameters to use for dataset (has to be from small_datasets)
    preproc_params = 3
    feature_ext_params = 1
    mid_dim_params = 1
    small_dim_params = 1
    params_list_data = [preproc_params, feature_ext_params, mid_dim_params, small_dim_params]

    # Define the sets of parameters to use for clustering labels (can be any of full, mid or small datasets on the same branch)
    preproc_params = 3
    feature_ext_params = 1
    # mid_dim_params = 1
    # small_dim_params = 1
    clustering_params = 1
    params_list_clusters = [preproc_params, feature_ext_params, clustering_params]

    # Define the audio clips to be used
    audio_path = 'middle_15'

    perform_visualization(params_path_data, params_path_clusters, params_list_data, params_list_clusters, audio_path)


    