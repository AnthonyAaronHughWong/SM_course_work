--import Text.Parsec.Prim(ParsecT,Stream)
--import Text.ParserCombinators.Parsec
--import Control.Arrow
import Control.Applicative
import Mylib




main = do
        trainData <- getData "trainTable.txt"
        let trainResult = trainWithData trainData
        print trainResult
        testData <- getData "testTable.txt"
        let result = classifier (fmap snd testData)  trainResult        
        print result
        let trueFalseTable = zipWith (==) (fmap fst testData) result
        print trueFalseTable
        print $ fromIntegral (length $ filter ( == True) trueFalseTable )
          / fromIntegral (length trueFalseTable)
        

