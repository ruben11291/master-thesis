#include <Ice/BuiltinSequences.ice>

module geocloud {
    exception AlreadyExists { string key; };
    exception NoSuchKey { string key; };
    //This interface provides a operation to get last modifications in a node
    interface Broker{
	void appendLog(string newLog);
	void startScenario(string scenario, int scen);
	void stopScenario(int scen);
	void cleanOrchestrator();
	void stopProcessors();
	
    };

    interface Processor{
	//int init( Broker * log);
        int l0(string path);
	int l0r(string path);
	int l1a(string path);
    };

    interface Orchestrator{
	//int init( Broker * log);
	int downloadedImage(string path);//the ground station calls this operation passing the path
	int levelProcessed(string path, string level);
	int imageProcessed(string path);
	void cleanQueue();
	
    };	
	
    interface ArchiveAndCataloge{
	//int init( Broker * log);
	int createScenario(string scenario);	
	int catalogue(string path,string scenario);
	int deleteScenario(string scenario);
    };
};
