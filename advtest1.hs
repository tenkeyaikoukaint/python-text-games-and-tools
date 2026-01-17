data Scene = Start | Entrance deriving(Show)
data Door = Opened | Closed deriving(Show, Eq)

data GameState = GameState { scene :: Scene
                           , door1 :: Door
                           , door2 :: Door } deriving (Show)

gs = GameState { scene = Start
               , door1 = Closed
               , door2 = Closed }

initmsg :: Scene -> String
initmsg Start = "スタート：あなたは家の前にいます。"
initmsg Entrance = "あなたは家の玄関にいます。"

cmdmsg :: Scene -> String -> GameState -> String
cmdmsg sc    "look" gs = look sc gs
cmdmsg Start   cmd  gs = msgstart cmd gs
cmdmsg Entrance cmd gs = msgent cmd gs

look :: Scene -> GameState -> String
look Start gs = "北に家が見えます。\n" ++ (if (door1 gs) == Closed
                                           then "ドアが閉じています。"
                                           else "ドアが開いています。" 
                                       )
look Entrance gs = "絵が飾ってあります。"

msgstart :: String -> GameState -> String
msgstart "open" gs = if (door1 gs) == Closed 
                         then "ドアが開きました。"
                         else "すでに開いています。"
msgstart "enter" gs = if (door1 gs) == Opened
                          then "家のなかに入りました。"
                          else "ドアが閉じています。"
msgstart cmd  gs = "すみませんが、その行動はできません。"

msgent :: String -> GameState -> String
msgent cmd gs = "それはできません。"

scexe :: Scene -> String -> GameState -> Scene
scexe sc cmd gs = sc

cmdexe :: Scene -> String -> GameState -> GameState
cmdexe Start cmd gs = cmdstart cmd gs
cmdexe Entrance cmd gs = cmdent cmd gs

cmdstart :: String -> GameState -> GameState
cmdstart "open" gs = if (door1 gs) == Closed
                         then gs {door1 = Opened }
                         else gs
cmdstart "enter" gs = if (door1 gs) == Opened
                          then gs {scene = Entrance}
                          else gs
cmdstart   cmd  gs = gs 

cmdent :: String -> GameState -> GameState
cmdent cmd gs = gs

routine :: GameState -> IO()
routine gs = do
    putStrLn $ initmsg (scene gs)
    putStrLn "command:"
    cmd <- getLine
    putStrLn (cmdmsg (scene gs) cmd gs)
    routine (cmdexe (scene gs) cmd gs)

main = do
    routine gs
