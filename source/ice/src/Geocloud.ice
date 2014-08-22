
module geocloud {
    exception AlreadyExists { string key; };
    exception NoSuchKey { string key; };
    exception CreationScenarioException{};
    exception StartScenarioException{};
    exception StopScenarioException{};
    exception DeleteScenarioException{};
    exception ArchiveNotAvailableException{};
    exception OrchestratorNotAvailableException{};
    exception ProcessingException{};
    exception CataloguingException{};

    //This interface provides a operation to get last modifications in a node

    interface Orchestrator{
    	void initScenario(int scen) throws StartScenarioException,ArchiveNotAvailableException;
	void downloadedImage(string path);//the ground station calls this operation passing the path
	void imageProcessed(string path);
	void imageCatalogued(string path);
	void stopScenario() throws StopScenarioException;
    };

    interface Broker{
	void startScenario(int scen) throws OrchestratorNotAvailableException, StartScenarioException;
	void appendLog(string newLog);
	void stopScenario(int scen);
	void setOrchestrator( Orchestrator * orch);
	string getLastLogs();
    };


 interface Processor{
	//int init( Broker * log);
       	void processImage(string path) throws ProcessingException;
	void shutdown();
	void setOrchestrator(Orchestrator * orch);
    };



    interface ArchiveAndCatalogue{
	void setBroker( Broker * bro);
	void createScenario(string scenario) throws CreationScenarioException;
	void catalogue(string path,string storage,string scenario) throws CataloguingException;
	void deleteScenario(int scenario) throws DeleteScenarioException;
    };
};
