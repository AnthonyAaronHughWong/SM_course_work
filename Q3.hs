import Mylib

{--
-- approximate distant function 
dis::Floating a => ((a,a), (a,a)) ->  a -> ClassId -> a  -> a
dis params sample classId eta = fst + log ( snd ** (1/eta))
  where fst = -1/2 *  p_sample c
        snd = exp $ eta * (1/2) * p_sample c2
        (c, c2) = if classId == A then params else (c2_t, c1_t)
                                    where (c1_t, c2_t) = params
        -- probability of a sample given the parameter
        p_sample = getProb sample

-- objective Q
objQ::Floating a => ((a,a), (a,a))-> a -> a -> [(ClassId, a)] -> a
objQ params eta alpha trainData = sum objs
                        where objs = fmap (step alpha . d) trainData
                              d = \(classId, sample) ->
                                    dis params sample classId eta

--}
-- dis on 3 dimension
disVector::Floating a => ([(a,a)], [(a,a)]) -> (ClassId, [a]) ->a
disVector params (classId, sample)= fst + snd
  where fst = -1/2 *  p_sample c
        snd = (1/2) * p_sample c2
        (c, c2) = if classId == A then params else (c2_t, c1_t)
                                    where (c1_t, c2_t) = params
        -- probability of a sample given the parameter
        p_sample = getProbVector sample


disPartialVector::Floating a => ([(a,a)], [(a,a)]) ->
                  (ClassId, [a]) -> ([(a,a)], [(a,a)])
disPartialVector params@(c1_t, c2_t) (classId, sample) =
  (paramDo (c1*0.5*) $ g_part c1_t, paramDo (c2*0.5*) $ g_part c2_t)
      where g_part = getProbPartialVector sample
            (c1, c2) = if classId == A then (-1, 1) else (-1,1)

-- objective Q on 3 dimension
objQVector::Floating a => ([(a,a)], [(a,a)]) -> a -> [(ClassId, [a])] -> a
objQVector params alpha trainData = sum objs
                        where objs = fmap (step alpha . disVector params)
                                     trainData


partialQ::Floating a =>  a -> [(ClassId, [a])] -> ([(a,a)],[(a,a)])->
    ([(a,a)], [(a,a)])
partialQ  alpha trainData params = paramsDo  (alpha*) $
                                foldl1 (paramsDo2 (+))  (fmap f trainData)
  where f x = paramsDo (*(coeff $ step_ $ disVector params x) )
              (disPartialVector params x)
        coeff l = l * (1-l)
        step_ = step alpha

graIter::Floating a =>  a -> [(ClassId, [a])] -> a -> ([(a,a)],[(a,a)])->
    ([(a,a)], [(a,a)])
graIter  alpha trainData delta params = newparams
  where off = partialQ alpha trainData params
        newparams = paramsDo2 (\x y -> x - delta * y) params off

-- approximate step function
step::Floating a => a -> a -> a
step alpha d = 1 / (1 +  exp ( - alpha * d) )


alpha = 0.5
delta = 1
printResult trainData testData trainResult =
  do
        print trainResult
        print $ calRatio trainData trainResult
        print $ objQVector trainResult alpha trainData
        print $ calRatio testData trainResult

main = do
        trainData <- getData "trainTable.txt"
        testData <- getData "testTable.txt"
        let trainResult = trainWithData trainData
        printResult trainData testData trainResult
        let getNew = graIter alpha trainData delta
        let iter trainResult =
              do
                let new =  getNew trainResult
                printResult trainData testData new
                return new
        foldl (>>=) (iter trainResult) (replicate 100 iter)
