from django.shortcuts import render

# Create your views here.

def getNextPathList(curUser: User, pathBuilder: Path) -> list:
	# returns alist of children paths relative to our current Path in FileTree
	nextPaths = []
	print("Get Next Path List ??")
	for _name in os.listdir(pathBuilder.path):
		subdir = os.path.join(pathBuilder.path, _name)
		if os.path.isdir(subdir):
			print(_name)
			nextPaths.append(_name)

	return nextPaths	

def updatePathNext(pid: int, nextPaths: list) -> None:
	# Updates a Path's 'NEXT" entry, such that a path has a LIST of its children $paths
	print("Updating Path.next [it] {}".format(str(pid)))
	_curPath = Path.objects.get(id=pid)
	# it = _curPath.next
	print("Looking at [it] {}".format(str(_curPath.path)))
	for _next in nextPaths:
		# it:NextPath = NextPath.objects.create(
		# 	data=_next
		# )
		new_next = _curPath.next_set.create(
			data=_next
		)
		print("FOUND Data: ",new_next.data)
		print("Register: {} -- {}".format(_curPath.path,new_next.data))
		# _curPath.
		# _curPath.save()


def getFilePathContext(request) -> dict:
	# path = []
	# cur_path = None
	builder = request.POST.get("$PATH")
	print("Builder: {}".format(builder))
	# current_path
	this_user = User.objects.get(id=request.user.id)
	nextPaths:list = []
	# default_path:Path = None
	default_path_builder: Path = Path.objects.get(user=this_user)
	# print(f"Most Recent Path: {default_path.path} \n\n")
	nextPaths = getNextPathList(curUser=this_user, pathBuilder=default_path_builder)
	context = {"pathBuilder":default_path_builder, "nextPathList": nextPaths}
	
	# return (cur_path,nextPaths)
	return context
	
def displaySetStoragePath(request):

	# 	# =(1) get All 'next' paths set up in DB.model
	# 	# (2) Set Storage mode to UPDATE
	# 	# (3) append new Path
	# pathDataDialog = PathDataDialog()
	this_user = User.objects.get(id=request.user.id)
	next_path_list = []
	_full_path=Path.objects.filter(user=this_user)
	print("FULL_PATH {}".format(_full_path))
	full_path=""
	# for data in _full_path:
	# 	full_path+=data.path 

	full_path += "/"+request.POST.get("$PATH")
	cur_path_builder: Path = None 
	# if no Path objects exist yet for this user
	# - we create one and peek at its children
	if Path.objects.filter(user=this_user).exists():
	# 	# turn on Storate update permissions.
		cur_path_builder = Path( 
			user=this_user,
			path= "/" + request.POST.get("$PATH"),
		)
		
	# 	next_path_list=getNextPathList(this_user, this_path.path)
		for _data in next_path_list:
			cur_path_builder.next=NextPath.objects.create(
				data=_data
			)
		# cur_path_builder.storage=StorageHandler(user=this_user, update=True).save()

		storage_rule = StorageHandler.objects.get(user=this_user)
		storage_rule.user=this_user
		storage_rule.update = True 
		if storage_rule.fullpath is None:
			storage_rule.fullpath = ""
		else:
			storage_rule.fullpath += "/" + request.POST.get("$PATH")
		storage_rule.save()

		cur_path_builder.storage = storage_rule
		cur_path_builder.save()

		next_path_list = getNextPathList(this_user, cur_path_builder)
		# storage_rule:StorageHandler = cur_path_builder
		# StorageHandler.objects.get(id=cur_path_builder.id)
		# storage_rule=StorageHandler.objects.get(user=this_user)
		# storage_rule.update=False
		# full_path = storage_rule.fullpath
		# storage_rule.save()
		# return {
		# "update_path_dialog":storage_rule.update,
		# "path": full_path, 
		# "nextpaths":next_path_list,
		# }
	elif Path.objects.filter(user=this_user).none():

		storage_rule = StorageHandler.objects.create(
					user=this_user,
					update=True
				)
		cur_path_builder = Path.objects.create(
				user=this_user,
				path=PathDataDialog.DEFAULT_PATH,
				storage=storage_rule
		)

	# mypath = Path.objects.get(user=this_user)
	nextPaths = []
	print("Get Next Path List ??")
	pathBuilder = "/"+request.POST.get("$PATH")
	for _name in os.listdir():
		subdir = os.path.join(pathBuilder, _name)
		if os.path.isdir(subdir):
			print(_name)
			nextPaths.append(_name)
	# storage_rule:StorageHandler = cur_path_builder
	# StorageHandler.objects.get(id=cur_path_builder.id)
	storage_rule=StorageHandler.objects.get(user=this_user)
	storage_rule.update=True
	full_path = storage_rule.fullpath
	storage_rule.save()
		# Path.objects.get(user=this_user)

	print("\n[Created New FilePath for User [{}]]".format(this_user.username))
	return {
		"update_path_dialog":StorageHandler.objects.get(user=this_user).update,
		"path": storage_rule.fullpath, 
		"nextpaths":nextPaths,
		}


def displayCurrentStorageView(request, aUser:User):
	current_path_builder = request.GET
	print("\n\nREQUEST: {}".format(current_path_builder))
	next_path_list: list = []
	default_path_builder: Path = None
	storage_rule: StorageHandler = None
	if "$EDIT" in request.GET:
		print("\n\n$edit REQUEST: {}".format(current_path_builder))
		if Path.objects.get(user=aUser).exists():
			default_path_builder = Path.objects.get(user=aUser)
			# print(f"Most Recent Path: {default_path_builder.path} \n\n")
			default_path_builder.storage.objects.update_or_Create(
				update=True
			)
			next_path_list = getNextPathList(curUser=aUser, pathBuilder=default_path_builder)
			context = {"pathBuilder":default_path_builder, "nextPathList": next_path_list}
			print("path-builder: {}".format(default_path_builder))
			print("\n\tNextPath: {}".format(next_path_list))
			storage_rule=default_path_builder.storage.objects.get(id=default_path_builder.id)
			next_path_list = getNextPathList(curUser=aUser, pathBuilder=default_path_builder)
			# make sure to turn off after editing..
			storage_rule.update_or_create(
				update=False
			)
			return render(request, 'core/home.html', {
				"update_path_dialog":True,
				"path":default_path_builder.path, 
				"nextpaths":next_path_list
				})

	else:
		if Path.objects.filter(user=aUser).exists():
			display = Path.objects.get(user=aUser)
			
			# display_storage_rule = storage_rule.objects.get(user=aUser)
			display_nextPathList = getNextPathList(aUser, display)
			return render(request, 'core/home.html', {
					"update_path_dialog":True,
					"path":display.path,
					"nextpaths":display_nextPathList
					})
		else:
			# display Default $Path info
			# display_storage_rule = StorageHandler.objects.get(user=aUser)
			return render(request, 'core/home.html', {
					"update_path_dialog":False,
					"path":PathDataDialog.DEFAULT_PATH,
					"nextpaths":[PathDataDialog.SENTINAL_OPEN_PATH]
					})
@login_required
def home(request):
	# path = None
	# cpath="/"
	pathDataDialog = PathDataDialog()
	this_user = User.objects.get(id=request.user.id)
	path_list = []
	print("REQUEST_post: ",request.POST)

	print("REQUEST_get: ",request.GET)

	if request.method == 'POST':
		if "$PATH" in request.POST:
			print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
			builder = request.POST.get("$PATH")
			print("\n\n%%%[MAIN__HOME.path-builder]: {}".format(builder))
			print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
			ui_context = displaySetStoragePath(request)
			return render(request, 'core/home.html', ui_context)
		else:
			print("[MAIN_HOME.request.isEMpty()]")
			
	elif request.method == 'GET':
		print("\n\nFound Path: {}".format(str(request.GET)))
		print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
		print("Request.GET")
		print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
		displayCurrentStorageView(request, this_user)
			
		next_path_list: list = []
		default_path_builder: Path = None
		storage_rule: StorageHandler = None
		if "$EDIT" in request.GET:
			print("\n\n$edit REQUEST: {}".format(request.GET))
			if Path.objects.get(user=this_user).exists():
				default_path_builder = Path.objects.get(user=this_user)
				# print(f"Most Recent Path: {default_path_builder.path} \n\n")
				default_path_builder.storage.objects.update_or_Create(
					update=True
				)
				next_path_list = getNextPathList(curUser=this_user, pathBuilder=default_path_builder)
				context = {"pathBuilder":default_path_builder, "nextPathList": next_path_list}
				print("path-builder: {}".format(default_path_builder))
				print("\n\tNextPath: {}".format(next_path_list))
				storage_rule=default_path_builder.storage.objects.get(id=default_path_builder.id)
				next_path_list = getNextPathList(curUser=this_user, pathBuilder=default_path_builder)
				# make sure to turn off after editing..
				storage_rule.update_or_create(
					update=False
				)
				return render(request, 'core/home.html', {
					"update_path_dialog":True,
					"path":default_path_builder.path, 
					"nextpaths":next_path_list
					})

		else: #no Request Query Params..
			if Path.objects.filter(user=this_user).exists():
				display = Path.objects.get(user=this_user)
				
				# display_storage_rule = storage_rule.objects.get(user=aUser)
				display_nextPathList = getNextPathList(this_user, display)
				return render(request, 'core/home.html', {
						"update_path_dialog":True,
						"path":display.path,
						"nextpaths":display_nextPathList
						})
			else:
				# display Default $Path info
				displayStorage = Path.objects.all()
				builder = {"fullpath":[]}
				stringifyBuilder = None
				# for displayPath in displayStorage:
				# 	builder["fullpath"].append(displayPath.path)
				# stringifyBuilder = json.dumps(builder)
				# display_storage_rule,created = StorageHandler.objects.get_or_create(user=this_user, 
				# 	update=True,
				# 	fullpath=stringifyBuilder,
				# )
				return render(request, 'core/home.html', {
						"update_path_dialog":True,
						"path":PathDataDialog.DEFAULT_PATH,
						"nextpaths":getNextPathList(this_user, Path(PathDataDialog.DEFAULT_PATH))
						})

	# return render(request, 'core/home.html', {
	# 		"path_dialog":pathDataDialog.showDialog(),
	# 		"path":"$PAth is empty!", 
	# 		"nextpaths":["$EDIT"]
	# 		})
