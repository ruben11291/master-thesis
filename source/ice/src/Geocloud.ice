#include <Ice/BuiltinSequences.ice>

module geocloud {
    exception AlreadyExists { string key; };
    exception NoSuchKey { string key; };
    //This interface provides a operation to get last modifications in a node
    interface Broker{
	void appendLog(string newLog);
	void startScenario(string scenario, int scen);
	void stopScenario(int scen);
    };

 
 interface Processor{
	//int init( Broker * log);
       	void processImage(string path);
	void shutdown();
    };	

    interface Orchestrator{
	int downloadedImage(string path);//the ground station calls this operation passing the path
	int levelProcessed(string path, Processor* pp, string level);
	int imageProcessed(string path, Processor* pp );
	void cleanQueue();
	void stop();
	
    };
	
    interface ArchiveAndCataloge{
	//int init( Broker * log);
	int createScenario(string scenario);	
	int catalogue(string path,string scenario);
	int deleteScenario(string scenario);
    };
};
