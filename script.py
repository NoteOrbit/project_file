import subprocess

def main():
    # Build and start the containers
    subprocess.run(["docker-compose", "up", "-d"])
    
    # Wait for the containers to start up
    print("Waiting for containers to start up...")
    subprocess.run(["docker-compose", "exec", "mongodb", "mongo", "--eval", "db.getCollectionNames()"])
    
    # Run the sc.py script to populate the database
    subprocess.run(["docker-compose", "exec", "backend", "python", "sc.py"])

if __name__ == '__main__':
    main()
