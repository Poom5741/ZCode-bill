import type { PluginScope, PluginsOverviewResult } from "@zcode/shared";
import { ServiceChannels } from "@zcode/shared";
import { createServiceDescriptor } from "../descriptors.js";

export interface IPluginsService {
  getOverview(params: {
    workspacePath: string;
    workspaceIdentity?: string;
  }): Promise<PluginsOverviewResult>;
  // Wave-1（ZBill 裁剪）：addMarketplace / removeMarketplace / updateMarketplace 管理方法
  // 已随插件市场 UI 与协议面一起删除；已安装插件的维护方法保留。
  installPlugin(params: {
    workspacePath: string;
    workspaceIdentity?: string;
    pluginName: string;
    marketplace: string;
    scope?: PluginScope;
  }): Promise<void>;
  uninstallPlugin(params: {
    workspacePath: string;
    workspaceIdentity?: string;
    pluginName: string;
    marketplace: string;
    scope?: PluginScope;
  }): Promise<void>;
  setPluginEnabled(params: {
    workspacePath: string;
    workspaceIdentity?: string;
    pluginName: string;
    marketplace: string;
    scope?: PluginScope;
    nativeScope?: "user" | "project" | "local";
    enabled: boolean;
  }): Promise<void>;
}

export const IPluginsService = createServiceDescriptor<IPluginsService>(ServiceChannels.Plugins);
