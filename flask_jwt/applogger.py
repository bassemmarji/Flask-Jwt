import os
import logging
import logging.config
import yaml

class applogger():
      logger = None

      default_path  = './static/logging.yaml'
      default_level = logging.INFO

      def __init__(self):
          # Logging Levels - 0 NOTSET / 10 DEBUG / 20 INFO / 30 WARN / 40 ERROR / 50 CRITICAL (Minimum priority Level Of Messages To Log)
          """Setup logging configuration"""
          path = self.default_path
          if os.path.exists(path):
              with open(path, 'rt') as f:
                   config = yaml.safe_load(f.read())
              logging.config.dictConfig(config)
          else:
              logging.basicConfig(level=self.default_level)

          self.logger = logging.getLogger(__name__)
          #print("Name Logger = " , __name__)
          #print("Logger Parent = ", self.logger.parent)


#logger = applogger()
#logger.debug("This is a debug message")
#logger.info("This is an info message")
#logger.error("This is an error message")
#logger.critical("This is a critical message")