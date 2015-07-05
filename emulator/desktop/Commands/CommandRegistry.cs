using System;
using System.Collections.Generic;
using System.Reflection;

namespace SuperSimonEmulator.Commands
{
    /// <summary>
    /// Represents the registry for commands within the system
    /// </summary>
    public static class CommandRegistry
    {
        private static Dictionary<byte, Type> _commandMapping = new Dictionary<byte, Type>();

        /// <summary>
        /// Attempts to find a command by ID. If the command is found then a new instance of
        /// the command is created for consumption.
        /// </summary>
        /// <param name="commandId">The command ID to lookup</param>
        /// <returns>The command instance created (if found), or null if the command ID is not registered</returns>
        public static Command FindCommand(byte commandId)
        {
            if (_commandMapping.Count == 0)
                FindCommands();
            if (_commandMapping.ContainsKey(commandId))
                return (Command)Activator.CreateInstance(_commandMapping[commandId]);
            return null;
        }

        private static void FindCommands()
        {
            var assembly = Assembly.GetAssembly(typeof(Command));
            foreach (var type in assembly.GetTypes())
            {
                if (typeof(Command).IsAssignableFrom(type) && !type.IsAbstract && type.IsPublic && !type.IsInterface && type.IsClass)
                {
                    Command instance = (Command)Activator.CreateInstance(type);
                    _commandMapping[instance.CommandId] = type;
                    Console.WriteLine("Registered " + type.Name + " as command with ID " + instance.CommandId);
                }
            }
        }
    }
}
