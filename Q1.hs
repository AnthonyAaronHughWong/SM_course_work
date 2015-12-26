--import Text.Parsec.Prim(ParsecT,Stream)
--import Text.ParserCombinators.Parsec
import Control.Arrow

data ClassId = A | B 
             deriving(Show, Read, Eq)
data GaussParam = GaussParam Double Double

mean::Floating a=>[a] -> a
mean d = sum d /  fromIntegral ( length d)

sigmaSq::Floating a=>[a] ->a
sigmaSq d = sum [ (j - m)^2 |j<-d] / l
        where m = mean d
              l = fromIntegral ( length d)

meanSigmaSq::Floating a=>[a]->(a,a)
-- meanSigmaSq = mean &&& sigmaSq
-- but only use mean once
meanSigmaSq d = (m, sum [ (j - m)^2 |j<-d] / l)
        where m = mean d
              l = fromIntegral ( length d)


--a Sample -> (mean, sigma) of a single guass -> Probability
getRelProb::Floating a=>a -> (a,a)->a
getRelProb d (m, sig) = exp ( - (d - m) ^ 2 / (sig * 2)) / sqrt sig 

--tree dimensional Sample -> tree dimensional of (mean, sigma) -> Probability product
getRelProbVector::Floating a=> [a] -> [(a,a)] -> a
getRelProbVector d p = product $ zipWith getRelProb d p

-- return (a,b), where a and b are lists (3 dimension) of (Double, Double), namely (mean, sigma)
trainWithData::Floating a => [(ClassId, [a])] -> ([(a, a)], [(a, a)])
trainWithData d = let (a,b) = splitTrainData d in
    (cal a, cal b)
    where v1 = fmap head
          v2 = fmap (!! 1)
          v3 = fmap (!! 2)
          f d = [v1 d, v2 d, v3 d]
          cal d= fmap meanSigmaSq (f d)

-- -> [InputVector] ->  trainedDate which contains parameters of gauss -> [ClassId]
classifier::(Floating a, Ord a)=> [[a]]-> ([(a,a)],[(a,a)] )-> [ClassId]
classifier d (p1, p2) = fmap (\x -> if getRelProbVector x p1 > getRelProbVector x p2 then A else B  ) d

-- splitTrainData according to their classId
splitTrainData::[(ClassId, [a])] -> ([[a]],[[a]])
splitTrainData d = (a, b)
        where a = [ k |   (j,k) <- d,  j == A]
              b = [ k |   (j,k) <- d,  j == B]



parseData d = fmap (\x -> (read $ head x,fmap read ( tail x ))) fields
        where fields = fmap words ( lines d )

getData:: String -> IO [(ClassId, [Double])]
getData s = parseData <$> readFile s


main = do
        trainData <- getData "trainTable.txt"
        let trainResult = trainWithData trainData in
            do
            print trainResult
            testData <- getData "testTable.txt"
            let result = classifier (fmap snd testData)  trainResult in
                do
                print result
                let trueFalseTable = zipWith (==) (fmap fst testData) result in
                    do 
                    print trueFalseTable
                    print $ fromIntegral (length $ filter ( == True)  trueFalseTable )  / fromIntegral (length trueFalseTable)
        

