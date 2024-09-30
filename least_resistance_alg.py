def least_resistance(start, end, d = 0):
  # breaks if already at the end
  if start == end:
    return [0, [start]]
  # sets default values, giving all adjoining nodes to start and end
  completed = False
  spaths = []
  for i in range(1,22):
    if data[d][start-1][i-1] != "":
      spaths.append([i])
  epaths = []
  for i in range(1,22):
    if data[d][i-1][end-1] != "":
      epaths.append([i])
  voltage = 0
  route = []
  # main loop, increases voltage and runs a series of checks
  while not completed:
    voltage += 1
    # for each set of paths, calculates residual voltage left over after subtracting resistance of each existing path
    for paths in spaths:
      residual = voltage
      for i in range(len(paths)):
        if i == 0:
          residual -= float(data[d][start-1][paths[0]-1])
        else:
          residual -= float(data[d][paths[i-1]-1][paths[i]-1])
      # checks if the residual is sufficient to complete another path
      for i in range(1, 22):
        if i != start and paths.count(i) == 0:
          if data[d][paths[len(paths)-1]-1][i-1] != "":
            if residual >= float(data[d][paths[len(paths)-1]-1][i-1]):
              # appends the path as long as it isn't a duplicate
              new_path = []
              for element in paths:
                new_path.append(element)
              new_path.append(i)
              duplicate = False
              for expaths in spaths:
                if expaths == new_path:
                  duplicate = True
              if not duplicate:
                spaths.append(new_path)
    # same implementation as above, but for the set of end paths
    for paths in epaths:
      residual = voltage
      for i in range(len(paths)):
        if i == 0:
          residual -= float(data[d][paths[0]-1][end-1])
        else:
          residual -= float(data[d][paths[i]-1][paths[i-1]-1])
      for i in range(1, 22):
        if i != end and paths.count(i) == 0:
          if data[d][i-1][paths[len(paths)-1]-1] != "":
            if residual >= float(data[d][i-1][paths[len(paths)-1]-1]):
              new_path = []
              for element in paths:
                new_path.append(element)
              new_path.append(i)
              duplicate = False
              for expaths in epaths:
                if expaths == new_path:
                  duplicate = True
                  break
              if not duplicate:
                epaths.append(new_path)
    # check condition for start and end paths meeting at a node
    checklist = [False] * 21
    for paths in spaths:
      checklist[paths[len(paths)-1]-1] = True
    for paths in epaths:
      if checklist[paths[len(paths)-1]-1]:
        # makes sure that the completion isn't from the default values with insufficient voltage
        if data[d][start-1][paths[len(paths)-1]-1] != "" and len(paths) == 1:
          if voltage * 2 <= float(data[d][start-1][paths[len(paths)-1]-1]) + float(data[d][paths[len(paths)-1]-1][end-1]):
            continue
        # creates the route by splicing together the start and reversed end path
        route.append(start)
        for paths_s in spaths:
          if paths_s[len(paths_s)-1] == paths[len(paths)-1]:
            for element in paths_s:
              route.append(element)
            break
        for i in range(len(paths)-2, -1, -1):
          route.append(paths[i])
        route.append(end)
        completed = True
        break
    # check condition for start and end paths meeting on a path
    for paths_s in spaths:
      # finds the residual of all possible start and end paths
      if not completed:
        sresidual = voltage
        for i in range(len(paths_s)):
          if i == 0:
            sresidual -= float(data[d][start-1][paths_s[0]-1])
          else:
            sresidual -= float(data[d][paths_s[i-1]-1][paths_s[i]-1])
        for paths_e in epaths:
          eresidual = voltage
          for j in range(len(paths_e)):
            if j == 0:
              eresidual -= float(data[d][paths_e[0]-1][end-1])
            else:
              eresidual -= float(data[d][paths_e[j]-1][paths_e[j-1]-1])
          # checks if the end nodes are adjoining and sum of residuals can span it
          if data[d][paths_s[len(paths_s)-1]-1][paths_e[len(paths_e)-1]-1] != "":
            if sresidual + eresidual > float(data[d][paths_s[len(paths_s)-1]-1][paths_e[len(paths_e)-1]-1]):
              # creates the route by splicing together the start and reversed end path
              route.append(start)
              for element in paths_s:
                route.append(element)
              for k in range(len(paths_e)-1, -1, -1):
                route.append(paths_e[k])
              route.append(end)
              completed = True
              break
  # calculates time using the paths from the route data
  time = 0
  for i in range(1, len(route)):
    time += float(data[d][route[i-1]-1][route[i]-1])
  # if start and end is connected, check this value against time
  if data[d][start-1][end-1] != "":
    if float(data[d][start-1][end-1]) < time:
      time = float(data[d][start-1][end-1])
      route = [start, end]

  return [time, route]
