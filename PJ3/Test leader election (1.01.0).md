1

Test leader election (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
```

 <span style="color:red">Test leader election with even nodes (0.0/1.0)</span>

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 0 expected: 1
```

Test server blocks on updatefile when majority is not available (3.0/3.0)

```
Started 5 server nodes
Checking isLeader, found: 1 expected: 1
LeaderID is 0
Calling updatefile() in leader
Crashing nodeId: 1
Crashing nodeId: 2
Crashing nodeId: 3
Testing if the server blocks on updatefile
```

Testing if most up to date node becomes leader (3.0/3.0)

```
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 3
Calling updatefile() in leader
Crashing nodeId: 0
Crashing nodeId: 1
Calling updatefile() in leader
Crashing nodeId: 2
Crashing nodeId: 3
Crashing nodeId: 4
Restoring nodeId: 0
Restoring nodeId: 1
Restoring nodeId: 3
Checking new leader, found: 3 expected: 3
```

Test no leader until a majority of nodes are up (3.0/3.0)

```
Started first server
Checking isLeader, found: 0 expected: 0
Started second server
Checking isLeader, found: 0 expected: 0
Started third server
Checking isLeader, found: 1 expected: 1
Started fourth server
Leader did not change
Started fifth server
Leader did not change
```

Test no leader until a majority of nodes are up with even nodes (3.0/3.0)

```
Started first server
Checking isLeader, found: 0 expected: 0
Started second server
Checking isLeader, found: 0 expected: 0
Started third server
Checking isLeader, found: 0 expected: 0
Started fourth server
Checking isLeader, found: 1 expected: 1
Started fifth server
Leader did not change
Started sixth server
Leader did not change
```

Test only leader can call updatefile() (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 2
Calling updatefile() in followers
Calling updatefile() in leader
Leader did not raise exception, leaderId 2
```

Test leader re-election (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
```

Test leader re-election while majority nodes are not crashed (2.0/2.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 0 expected: 0
```

 <span style="color:red">Test leader re-election while majority nodes are not crashed with even nodes (0.0/2.0)</span>

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 0 expected: 1
```

Test leader re-election with even nodes (1.0/1.0)

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
```

Test version in crashed and restored followers gets updated (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 1
Calling updatefile() in leader
Crashing nodeId: 0
Calling updatefile() in leader
Version correct on crashed follower, found: 1 expected: 1
Restoring nodeId: 0
Version correct on restored follower, found: 3 expected: 3
```

Test leader remains same as long as it is running (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing a follower
Leader did not change
Crashing a follower
Leader did not change
```

Test version in followers gets updated after updatefile (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 1
Calling updatefile() in leader
```









2

Test leader election (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
```

Test leader election with even nodes (1.0/1.0)

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
```

Test server blocks on updatefile when majority is not available (3.0/3.0)

```
Started 5 server nodes
Checking isLeader, found: 1 expected: 1
LeaderID is 1
Calling updatefile() in leader
Crashing nodeId: 0
Crashing nodeId: 2
Crashing nodeId: 3
Testing if the server blocks on updatefile
```

Testing if most up to date node becomes leader (3.0/3.0)

```
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 1
Calling updatefile() in leader
Crashing nodeId: 0
Crashing nodeId: 2
Calling updatefile() in leader
Crashing nodeId: 1
Crashing nodeId: 3
Crashing nodeId: 4
Restoring nodeId: 0
Restoring nodeId: 2
Restoring nodeId: 1
Checking new leader, found: 1 expected: 1
```

Test no leader until a majority of nodes are up (3.0/3.0)

```
Started first server
Checking isLeader, found: 0 expected: 0
Started second server
Checking isLeader, found: 0 expected: 0
Started third server
Checking isLeader, found: 1 expected: 1
Started fourth server
Leader did not change
Started fifth server
Leader did not change
```

Test no leader until a majority of nodes are up with even nodes (3.0/3.0)

```
Started first server
Checking isLeader, found: 0 expected: 0
Started second server
Checking isLeader, found: 0 expected: 0
Started third server
Checking isLeader, found: 0 expected: 0
Started fourth server
Checking isLeader, found: 1 expected: 1
Started fifth server
Leader did not change
Started sixth server
Leader did not change
```

Test only leader can call updatefile() (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 2
Calling updatefile() in followers
Calling updatefile() in leader
Leader did not raise exception, leaderId 2
```

Test leader re-election (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
```

Test leader re-election while majority nodes are not crashed (0.0/2.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 0 expected: 1
```

Test leader re-election while majority nodes are not crashed with even nodes (2.0/2.0)

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 0 expected: 0
```

Test leader re-election with even nodes (1.0/1.0)

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
```

Test version in crashed and restored followers gets updated (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 1
Calling updatefile() in leader
Crashing nodeId: 0
Calling updatefile() in leader
Version correct on crashed follower, found: 1 expected: 1
Restoring nodeId: 0
Version correct on restored follower, found: 3 expected: 3
```

Test leader remains same as long as it is running (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing a follower
Leader did not change
Crashing a follower
Leader did not change
```

Test version in followers gets updated after updatefile (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 4
Calling updatefile() in leader
```





3


Test leader election (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
```

Test leader election with even nodes (1.0/1.0)

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
```

Test server blocks on updatefile when majority is not available (3.0/3.0)

```
Started 5 server nodes
Checking isLeader, found: 1 expected: 1
LeaderID is 0
Calling updatefile() in leader
Crashing nodeId: 1
Crashing nodeId: 2
Crashing nodeId: 3
Testing if the server blocks on updatefile
```

Testing if most up to date node becomes leader (0.0/3.0)

```
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 4
Calling updatefile() in leader
Crashing nodeId: 0
Crashing nodeId: 1
Calling updatefile() in leader
Crashing nodeId: 2
Crashing nodeId: 3
Crashing nodeId: 4
Restoring nodeId: 0
Restoring nodeId: 1
Restoring nodeId: 2
Checking new leader, found: 1 expected: 2
```

Test no leader until a majority of nodes are up (3.0/3.0)

```
Started first server
Checking isLeader, found: 0 expected: 0
Started second server
Checking isLeader, found: 0 expected: 0
Started third server
Checking isLeader, found: 1 expected: 1
Started fourth server
Leader did not change
Started fifth server
Leader did not change
```

Test no leader until a majority of nodes are up with even nodes (3.0/3.0)

```
Started first server
Checking isLeader, found: 0 expected: 0
Started second server
Checking isLeader, found: 0 expected: 0
Started third server
Checking isLeader, found: 0 expected: 0
Started fourth server
Checking isLeader, found: 1 expected: 1
Started fifth server
Leader did not change
Started sixth server
Leader did not change
```

Test only leader can call updatefile() (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 1
Calling updatefile() in followers
Calling updatefile() in leader
Leader did not raise exception, leaderId 1
```

Test leader re-election (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
```

Test leader re-election while majority nodes are not crashed (2.0/2.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 0 expected: 0
```

Test leader re-election while majority nodes are not crashed with even nodes (2.0/2.0)

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 0 expected: 0
```

Test leader re-election with even nodes (1.0/1.0)

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
```

Test version in crashed and restored followers gets updated (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 3
Calling updatefile() in leader
Crashing nodeId: 0
Calling updatefile() in leader
Version correct on crashed follower, found: 1 expected: 1
Restoring nodeId: 0
Version correct on restored follower, found: 3 expected: 3
```

Test leader remains same as long as it is running (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing a follower
Leader did not change
Crashing a follower
Leader did not change
```

Test version in followers gets updated after updatefile (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 3
Calling updatefile() in leader
```





4

Test leader election (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
```

Test leader election with even nodes (1.0/1.0)

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
```

Test server blocks on updatefile when majority is not available (3.0/3.0)

```
Started 5 server nodes
Checking isLeader, found: 1 expected: 1
LeaderID is 3
Calling updatefile() in leader
Crashing nodeId: 0
Crashing nodeId: 1
Crashing nodeId: 2
Testing if the server blocks on updatefile
```

Testing if most up to date node becomes leader (3.0/3.0)

```
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 2
Calling updatefile() in leader
Crashing nodeId: 0
Crashing nodeId: 1
Calling updatefile() in leader
Crashing nodeId: 2
Crashing nodeId: 3
Crashing nodeId: 4
Restoring nodeId: 0
Restoring nodeId: 1
Restoring nodeId: 2
Checking new leader, found: 2 expected: 2
```

Test no leader until a majority of nodes are up (3.0/3.0)

```
Started first server
Checking isLeader, found: 0 expected: 0
Started second server
Checking isLeader, found: 0 expected: 0
Started third server
Checking isLeader, found: 1 expected: 1
Started fourth server
Leader did not change
Started fifth server
Leader did not change
```

Test no leader until a majority of nodes are up with even nodes (3.0/3.0)

```
Started first server
Checking isLeader, found: 0 expected: 0
Started second server
Checking isLeader, found: 0 expected: 0
Started third server
Checking isLeader, found: 0 expected: 0
Started fourth server
Checking isLeader, found: 1 expected: 1
Started fifth server
Leader did not change
Started sixth server
Leader did not change
```

Test only leader can call updatefile() (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 1
Calling updatefile() in followers
Calling updatefile() in leader
Leader did not raise exception, leaderId 1
```

Test leader re-election (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
```

Test leader re-election while majority nodes are not crashed (2.0/2.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 0 expected: 0
```

Test leader re-election while majority nodes are not crashed with even nodes (2.0/2.0)

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 0 expected: 0
```

Test leader re-election with even nodes (1.0/1.0)

```
Started 6 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing the leader
Checking isLeader, found: 1 expected: 1
```

Test version in crashed and restored followers gets updated (3.0/3.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
LeaderID is 1
Calling updatefile() in leader
Crashing nodeId: 0
Calling updatefile() in leader
Version correct on crashed follower, found: 1 expected: 1
Restoring nodeId: 0
Version correct on restored follower, found: 3 expected: 3
```

Test leader remains same as long as it is running (1.0/1.0)

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 1 expected: 1
Crashing a follower
Leader did not change
Crashing a follower
Leader did not change
```

<span style = "color:red">Test version in followers gets updated after updatefile (0.0/3.0)</span>

```
Started 5 server nodes
Checking number of leaders
Checking isLeader, found: 0 expected: 1
```